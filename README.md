# PDF Customizer

A Python toolset for customizing and splitting PDF documents, with a focus on generating personalized AI Readiness Reports from a master report. Built with [pypdf](https://pypdf.readthedocs.io/).

## Features

- **Exploring AI report** — Produce a single personalized report that keeps the "Exploring AI" summary and removes other personality summaries (pages 11–13).
- **Personality-specific reports** — Generate one report per personality type: **Exploring**, **Building**, **Integrating**, and **Leading**.
- **Configurable page ranges** — Use the CLI to specify custom page ranges for splitting.
- **Batch generation** — Create the full suite of personality reports in one run.

## Requirements

- Python 3.10+
- [pypdf](https://pypdf.readthedocs.io/) (see `requirements.txt`)

## Installation

```bash
# Clone the repository
git clone https://github.com/mawkunnmyat/PDF-Customizer.git
cd PDF-Customizer

# Create and activate a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### 1. Split PDF (CLI) — `split_pdf.py`

Flexible PDF splitter with configurable page ranges. Default behaviour: keep pages 1–10 and 14–end; skip pages 11–13.

```bash
# Default input/output and page ranges
python split_pdf.py

# Custom input and output files
python split_pdf.py input.pdf output.pdf

# Custom page ranges (e.g. first range 1–10, skip 11–13)
python split_pdf.py input.pdf output.pdf --first-range 1 10 --skip-range 11 13

# Quiet mode (no progress messages)
python split_pdf.py --quiet
```

### 2. Exploring AI report only — `generate_report.py`

Generates a single PDF that includes the intro, the "Exploring AI" summary (pages 1–10), and the deep dives + outro (from page 14). Pages 11–13 are omitted.

```bash
python generate_report.py
```

**Config (in script):**  
- Input: `STT25_7806_AI_Readiness_Report_v2.pdf`  
- Output: `STT25_Personalised_Exploring_AI.pdf`

### 3. Single personality report — `generate_all_reports.py`

Generates personalized reports for **Exploring**, **Building**, and **Integrating** (three reports per run).

```bash
python generate_all_reports.py
```

### 4. Full suite (all four personalities) — `generate_complete_suite.py`

Generates all four personality-specific reports: **Exploring**, **Building**, **Integrating**, and **Leading**.

```bash
python generate_complete_suite.py
```

**Output files:**

- `STT25_Personalised_Exploring_AI.pdf`
- `STT25_Personalised_Building_AI.pdf`
- `STT25_Personalised_Integrating_AI.pdf`
- `STT25_Personalised_Leading_AI.pdf`

## Project structure

| File | Description |
|------|-------------|
| `split_pdf.py` | CLI for splitting PDFs with configurable page ranges |
| `generate_report.py` | Produces the "Exploring AI" only report |
| `generate_all_reports.py` | Produces Exploring, Building, and Integrating reports |
| `generate_complete_suite.py` | Produces all four personality reports |
| `requirements.txt` | Python dependencies (pypdf) |

## Input PDF layout (expected)

The scripts assume the master report has:

- **Pages 1–9:** Common intro  
- **Page 10:** Exploring AI summary  
- **Page 11:** Building AI summary  
- **Page 12:** Integrating AI summary  
- **Page 13:** Leading AI summary  
- **Pages 14–end:** Deep dives and conclusion  

Adjust page indices in the scripts if your source PDF differs.

## License

This project is provided as-is. Use and modify according to your needs.

## Repository

- **GitHub:** [https://github.com/mawkunnmyat/PDF-Customizer](https://github.com/mawkunnmyat/PDF-Customizer)
