# The Explainer

A Python tool that analyzes PDF docum3. Install Python dependencies:

```bash
uv pip install PyPDF2
```

using local LLMs (via Ollama) from different professional perspectives to help non-experts understand complex documents.

## 🎯 Purpose

The Explainer helps laypeople (patients, clients, customers) understand complex PDF documents by providing expert analysis from various professional viewpoints. Whether it's a legal contract, medical report, tax document, or any other professional document, this tool breaks it down into understandable insights.

## ✨ Features

- **PDF Text Extraction**: Extracts text content from PDF files using PyPDF2
- **Professional Role-Based Analysis**: Analyzes documents from the perspective of different experts (lawyers, doctors, tax advisors, etc.)
- **Local LLM Processing**: Uses Ollama for privacy-focused, offline document analysis
- **Structured Output**: Generates well-formatted Markdown reports with consistent sections
- **Easy-to-Use CLI**: Simple command-line interface for quick document analysis

## 📋 Analysis Structure

Each analysis includes four key sections:

1. **Important Points** (Wichtige Punkte) - Key information to pay attention to
2. **Potential Pitfalls** (Potenzielle Fallstricke) - Clauses or sections that could be disadvantageous
3. **Advantages for Customer** (Vorteile für den Kunden) - Beneficial content for the reader
4. **Disadvantages for Customer** (Nachteile für den Kunden) - Content that could lead to disadvantages

## 🛠️ Prerequisites

### Required Software

1. **Python 3.13+** - The script requires Python 3.13 or higher
2. **Ollama** - Local LLM runtime

```bash
# Install Ollama (macOS)
brew install ollama

# Start Ollama service
ollama serve

# Pull the default model (llama3)
ollama pull llama3
```

## Python Dependencies

```bash
pip install PyPDF2
```

## 🚀 Installation

1. Clone or download this repository
2. Ensure Python 3.13+ is installed
3. Install Ollama and pull a model
4. Install Python dependencies:

```bash
pip install PyPDF2
```

## 💡 Usage

### Basic Usage

1. Run the script:

    ```bash
    python analyze_pdf_with_ollama.py
    ```

2. Enter the path to your PDF document when prompted
3. Specify the professional role for analysis (e.g., "Jurist", "Arzt", "Steuerberater")
4. Wait for the analysis to complete
5. Find the output in a `.analyzed.md.txt` file next to your original PDF

### Example Session

```text
📄 PDF Analyse mit lokalem LLM (Ollama)
Gib den Pfad zum PDF-Dokument ein: ~/Documents/contract.pdf
Welche Rolle soll das LLM einnehmen? (z. B. Jurist, Arzt, Steuerberater): Jurist

🔍 Lese PDF ein...
🧠 Erzeuge Prompt...
🚀 Führe Analyse durch mit Modell: llama3

✅ Analyse gespeichert unter: /Users/username/Documents/contract.analyzed.md.txt
```

## 📁 Project Structure

```text
the-explainer/
├── analyze_pdf_with_ollama.py  # Main application script
├── pyproject.toml              # Project configuration
└── README.md                   # This file
```

## 🔧 How It Works

1. **PDF Text Extraction**: Uses PyPDF2 to extract text from all pages of the PDF
2. **Prompt Generation**: Creates a structured prompt asking the LLM to analyze the document from a specific professional perspective
3. **LLM Analysis**: Sends the prompt to Ollama using the llama3 model (configurable)
4. **Output Generation**: Saves the structured analysis as a Markdown file

## 🎛️ Configuration

### Changing the LLM Model

The default model is `llama3`. To use a different model, modify the `model` parameter in the `run_ollama()` function call in `main()`, or update the function signature to accept different models.

### Supported Professional Roles

The tool works with any professional role you specify. Popular examples include:

- Jurist (Lawyer)
- Arzt (Doctor)
- Steuerberater (Tax Advisor)
- Finanzberater (Financial Advisor)
- Versicherungsexperte (Insurance Expert)
- Immobilienmakler (Real Estate Agent)

## ⚠️ Limitations

- Requires Ollama to be installed and running
- PDF text extraction quality depends on the source document
- Analysis quality depends on the chosen LLM model
- Currently supports German language prompts and analysis
- Large documents may take longer to process

## 🛡️ Privacy

This tool processes documents entirely locally using Ollama, ensuring your sensitive documents never leave your machine.

## 🤝 Contributing

Feel free to contribute by:

- Adding support for more document formats
- Implementing different output formats
- Adding multilingual support
- Improving error handling
- Optimizing performance

## 📄 License

This project is open source. Please check the license file for details.

## 🆘 Troubleshooting

### Common Issues

#### "Ollama command not found"

- Make sure Ollama is installed and in your PATH
- Try running `ollama --version` to verify installation

#### "Model not found"

- Pull the required model: `ollama pull llama3`
- Or specify a different model you have available

#### "No readable content found in PDF"

- The PDF might be image-based or encrypted
- Try with a different PDF file
- Consider using OCR tools for image-based PDFs

#### "File not found"

- Check the file path you entered
- Use absolute paths or ensure you're in the correct directory
- The tool supports `~` for home directory expansion
