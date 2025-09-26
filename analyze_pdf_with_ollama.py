import sys
import subprocess
from pathlib import Path
import PyPDF2


def get_pdf_text(pdf_path):
    try:
        print(f"📖 Öffne PDF-Datei: {pdf_path.name}")
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            total_pages = len(reader.pages)
            print(f"📄 Gefunden: {total_pages} Seite(n)")

            text_parts = []
            for i, page in enumerate(reader.pages, 1):
                print(f"📝 Verarbeite Seite {i}/{total_pages}...", end="", flush=True)
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
                    print(f" ✅ ({len(page_text)} Zeichen)")
                else:
                    print(" ⚠️ (leer)")

            full_text = "\n".join(text_parts)
            print(f"📊 Gesamt extrahierte Zeichen: {len(full_text)}")
            return full_text.strip()
    except Exception as e:
        print(f"❌ Fehler beim Auslesen des PDFs: {e}")
        sys.exit(1)


def build_prompt(role, document_text, language="de"):
    """Erzeugt den Prompt für das LLM.

    Parameters
    ----------
    role : str
        Expertenrolle (z.B. Jurist, Arzt, Steuerberater)
    document_text : str
        Vollständiger extrahierter Dokumententext
    language : str, optional
        ISO Sprachcode für die Ausgabe (z.B. 'de' oder 'en'). Standard: 'de'.
        Unterstützte Werte sind frei – wird direkt an das Modell weitergegeben.
    """

    language_instruction = {
        "de": "Die Ausgabe MUSS auf Deutsch erfolgen.",
        "en": "The output MUST be in English.",
        "fr": "La sortie DOIT être en français.",
        "es": "La salida DEBE estar en español.",
    }.get(language.lower(), f"The output MUST be in language code: {language}")

    return f"""Du bist ein sehr erfahrener {role}. Bitte analysiere das folgende Dokument kritisch aus der Sicht dieser Rolle.

Sprache der Analyse: {language}
{language_instruction}

### Ziel
Unterstütze einen Laien (z.B. Patient, Mandant oder Kunde), der dieses Dokument erhalten hat. Gehe dazu auf folgende Punkte ein:

1. **Wichtige Passagen** – besonders relevante Punkte, auf die unbedingt geachtet werden sollte.
2. **Fallstricke** – Formulierungen oder Abschnitte, die sich nachteilig auswirken könnten.
3. **Vorteile** – Inhalte, die vorteilhaft für den Leser sind.
4. **Nachteile** – Inhalte, die zu Nachteilen führen könnten.

### Ausgabeformat
Erstelle eine Markdown-Struktur mit (übersetze Überschriften bei anderer Sprache):
- ## Wichtige Punkte / Key Points
- ## Potenzielle Fallstricke / Potential Pitfalls
- ## Vorteile für den Kunden / Advantages
- ## Nachteile für den Kunden / Disadvantages

Falls die gewählte Ausgabesprache nicht Deutsch ist, übersetze konsistent alle Überschriften und Inhalte in die Zielsprache.

### Dokumentinhalt
Analysiere den folgenden Text:

{document_text}
"""


def run_ollama(prompt, model="llama3-gradient:8b"):  # alternatives: gemma3, gpt-oss
    try:
        print(f"🤖 Starte Ollama mit Modell: {model}")
        print(f"📏 Prompt-Länge: {len(prompt)} Zeichen")
        print("⏳ Warte auf Antwort von Ollama...")
        print("" + "=" * 50)
        print("🔄 OLLAMA OUTPUT (Live):")
        print("" + "=" * 50)

        # Start Ollama process with live output
        process = subprocess.Popen(
            ["ollama", "run", model],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
        )

        # Send prompt to process
        if process.stdin:
            process.stdin.write(prompt)
            process.stdin.close()

        output_lines = []
        error_lines = []

        # Read output line by line for real-time display
        while True:
            # Check if process is still running
            poll_result = process.poll()

            # Read available output
            try:
                if process.stdout:
                    line = process.stdout.readline()
                    if line:
                        print(line, end="", flush=True)  # Print in real-time
                        output_lines.append(line)
                    elif poll_result is not None:
                        # Process finished and no more output
                        break
            except Exception:
                if poll_result is not None:
                    break

        # Read any remaining stderr
        if process.stderr:
            stderr_output = process.stderr.read()
            if stderr_output:
                error_lines.append(stderr_output)

        # Wait for process to complete
        return_code = process.wait()

        print("" + "=" * 50)
        print(f"✅ Ollama beendet (Exit Code: {return_code})")

        if return_code != 0:
            error_msg = "".join(error_lines)
            print(f"❌ Fehler bei der LLM-Ausführung: {error_msg}")
            sys.exit(1)

        result = "".join(output_lines).strip()
        print(f"📊 Antwort-Länge: {len(result)} Zeichen")
        return result

    except FileNotFoundError:
        print("❌ Ollama nicht gefunden! Bitte installiere Ollama erst.")
        print("💡 Installation: brew install ollama")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unerwarteter Fehler bei der LLM-Ausführung: {e}")
        sys.exit(1)


def save_markdown_output(output_text, output_path):
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(output_text)
        print(f"\n✅ Analyse gespeichert unter: {output_path}")
    except Exception as e:
        print(f"Fehler beim Speichern der Datei: {e}")
        sys.exit(1)


def main():
    print("📄 PDF Analyse mit lokalem LLM (Ollama)")

    pdf_path_input = input("Gib den Pfad zum PDF-Dokument ein: ").strip()
    role = input(
        "Welche Rolle soll das LLM einnehmen? (z. B. Jurist, Arzt, Steuerberater): "
    ).strip()
    language = (
        input(
            "In welcher Sprache soll die Analyse ausgegeben werden? (z. B. de, en, fr) [de]: "
        ).strip()
        or "de"
    )
    print(f"🌐 Gewählte Ausgabesprache: {language}")

    # Pfad verarbeiten
    print(f"\n🔍 Verarbeite Pfad: {pdf_path_input}")
    pdf_path = Path(pdf_path_input).expanduser().resolve()
    print(f"📁 Vollständiger Pfad: {pdf_path}")

    if not pdf_path.exists():
        print(f"❌ Datei nicht gefunden: {pdf_path}")
        sys.exit(1)

    file_size = pdf_path.stat().st_size
    print(f"📊 Dateigröße: {file_size:,} Bytes ({file_size / 1024:.1f} KB)")

    # PDF einlesen
    print("\n" + "=" * 50)
    print("🔍 SCHRITT 1: PDF EINLESEN")
    print("" + "=" * 50)
    pdf_text = get_pdf_text(pdf_path)

    if not pdf_text:
        print("❌ Keine lesbaren Inhalte im PDF gefunden.")
        sys.exit(1)

    # Prompt erstellen
    print("\n" + "=" * 50)
    print("🧠 SCHRITT 2: PROMPT ERSTELLEN")
    print("" + "=" * 50)
    print(f"👤 Gewählte Expertenrolle: {role}")
    print("📝 Erstelle strukturierten Prompt...")
    prompt = build_prompt(role, pdf_text, language=language)
    print(f"✅ Prompt erstellt ({len(prompt)} Zeichen, Sprache: {language})")

    # Ollama ausführen
    print("\n" + "=" * 50)
    print("🚀 SCHRITT 3: ANALYSE DURCH OLLAMA")
    print("" + "=" * 50)
    analysis_output = run_ollama(prompt)

    # Ergebnis speichern
    print("\n" + "=" * 50)
    print("💾 SCHRITT 4: ERGEBNIS SPEICHERN")
    print("" + "=" * 50)
    output_txt_path = pdf_path.with_suffix(".analyzed.md.txt")
    print(f"📂 Ziel-Datei: {output_txt_path.name}")
    save_markdown_output(analysis_output, output_txt_path)

    print("\n" + "=" * 50)
    print("🎉 ANALYSE ABGESCHLOSSEN!")
    print("" + "=" * 50)
    print(f"📄 Original: {pdf_path.name}")
    print(f"📝 Analyse: {output_txt_path.name}")
    print(f"👤 Rolle: {role}")
    print(f"📊 Analyse-Länge: {len(analysis_output)} Zeichen")
    print(f"🌐 Sprache: {language}")


if __name__ == "__main__":
    main()
