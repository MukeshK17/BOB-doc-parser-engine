# Doc-Parser Interactive Risk Engine
**Automated Fraud Risk Parser for Financial Management Reports (FMRs)**

An end-to-end, 100% air-gapped document processing pipeline designed to automate compliance auditing for bank investigation reports and FMRs. The engine utilizes a high-performance "Waterfall" extraction model and a Dual-Stream tracking architecture to flag high-risk documents instantly, outputting executive PDF summaries and comprehensive CSV grids.

> 🏢 **Project Overview:** This enterprise solution was commissioned and developed for **Bank of Baroda** during an internal engineering residency/internship framework to solve structural auditing bottlenecks in high-security, network-isolated environments.

## ✨ Key Features
* **Dual-Path Text Extraction:** Rapid native digital text extraction via `PyMuPDF`, with automatic fallback to deep learning vision models (`PaddleOCR`) for flattened images and scanned documents.
* **Dual-Stream Analytics:** * *Stream 1:* Deterministic counting of 12 primary fraud-risk keywords with automated template-bias subtraction.
  * *Stream 2:* A dynamic, typo-tolerant Interactive Query Engine powered by Levenshtein distance string matching.
* **Automated Deliverables:** Generates conditional row-highlighted CSV tracking sheets and professional ReportLab PDF executive summaries.
* **Physical Segregation:** Automatically routes physical files into `/flagged` or `/clean` directories based on compliance logic.
* **Streamlit Dashboard:** A clean, user-friendly graphical interface for operators to upload zips/pdfs, set query constraints, and download reports locally.

## 📂 Repository Structure

```text
├── data/                    # Local workspace (Git-ignored for security)
│   ├── input/               # Drop target PDFs or ZIPs here
│   ├── output/              # Raw JSON analytical metric caches
│   ├── sorted/              # Physically segregated files (flagged/clean)
│   └── summary/             # Final CSV and PDF executive reports
├── src/
│   ├── analysis/
│   │   ├── fuzzy_match.py   # Levenshtein distance algorithm engine
│   │   └── regex_engine.py  # Typo-tolerant dynamic query compiler
│   ├── extraction/
│   │   ├── image_to_text.py # PaddleOCR fallback pipeline
│   │   └── native_text.py   # PyMuPDF fast-extraction pipeline
│   └── reporting/
│       ├── pdf_reporter.py  # ReportLab visual canvas generator
│       └── reporting.py     # Dual-stream counting & CSV generation
├── app.py                   # Streamlit Web Dashboard
├── config.py                # Global keywords, biases, & REJECS patterns
├── main.py                  # Headless CLI Orchestrator
├── boblogo.jpg              # UI Asset
├── requirements.txt         # Project dependencies
├── .gitignore               # Git exclusion rules for data privacy
└── README.md                # Project documentation
```
## Installation and Setup
1. Clone the repository:
```
git clone [https://github.com/MukeshK17/BOB-doc-parser-engine.git](https://github.com/MukeshK17/BOB-doc-parser-engine.git)
cd doc-parser-update
```
2. Create and activate a virtual environment:
```
python -m venv .venv

# On macOS/Linux:
source .venv/bin/activate  

# On Windows:
.venv\Scripts\activate
```
3. Install Dependencies
```
 pip install -r requirements.txt 
```

## Usage
### Interactive Web Dashboard

Launch the Streamlit graphical user interface locally:
```
streamlit run app.py
```
- Upload Files: Drop individual .pdf files, multiple selected files, or a compressed .zip archive into the sidebar file interface target area.

- Define Constraints: Input your interactive evaluation text prompt inside the custom text field container.

- Export Summary: View the live data frame grid directly inside the primary window container, and choose between downloading the full spreadsheet workbook track or generating the executive styled report document canvas.

## License

### This project is licensed under the terms of the open-source MIT License.