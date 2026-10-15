# JomiCheck Lite — Check Before You Buy

A beginner-friendly Streamlit prototype for **LandTech 2026, P5: Citizen Pre-Purchase Verification**. It lets a user search fictional land plot/deed records, review the recorded fields, read ownership history, and see transparent rule-based warnings.

> **Important:** Educational prototype using synthetic data. Not an official land-record verification service. No government system is connected. A result with no flags does not prove a plot is legally clear or fraud-free.

## Features

- 21 fictional deed records covering 20 unique plot IDs.
- Exact search by plot ID or deed ID (case-insensitive).
- Plot/deed details: recorded owner, plot ID, deed ID, land area, location, registration date, mutation status, deed status and acquisition status.
- Chronological ownership-history timeline.
- Transparent rules for multiple active deeds, incomplete mutation, listed cases, non-clear acquisition status and non-active deed status.
- Three prepared demo scenarios:
  - `P-1001` — no flags raised by the sample rules.
  - `P-1002` — mutation pending.
  - `P-1018` — two active deed entries associated with one plot.
- JSON file storage; no database or external service required.

## Requirements

- Python 3.10 or newer (Python 3.11 is a good choice).
- Internet access only to install Streamlit the first time. The app itself uses local JSON data and does not call external APIs.

## Run on Windows

Open PowerShell or Command Prompt in the `jomicheck_lite` folder:

```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL printed in the terminal (normally `http://localhost:8501`).

If `py` is not available, use `python` instead. If PowerShell blocks activation, open Command Prompt and run `.venv\Scripts\activate.bat`.

## Run on macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

## Test the data and warning rules

The small test suite uses Python's built-in `unittest` and does not require launching Streamlit:

```bash
python -m unittest discover -v
```

Validate the data file with:

```bash
python -m json.tool data/plots.json
```

Manual app checks:

1. Search `P-1001` — expected text: `No flagged issues in demo data`.
2. Search `P-1002` — expected a mutation-not-completed warning.
3. Search `P-1018` — expected a multiple-active-deeds warning.
4. Search `D-2026-1001` — expected to find plot `P-1001`.
5. Search `P-9999` — expected a friendly no-record message.

## Deploy with Streamlit Community Cloud

1. Create a GitHub repository and upload the contents of this project folder (keep `app.py`, `data_logic.py`, `requirements.txt`, and the `data/` folder at the repository root as shown).
2. Go to [Streamlit Community Cloud](https://share.streamlit.io/) and sign in with GitHub.
3. Choose **Create app**, then select your repository and branch.
4. Set the main file path to `app.py`.
5. Deploy. Streamlit installs the packages listed in `requirements.txt` and runs the app.
6. Open the generated app URL and test the three scenarios above.

No secrets or API keys are needed. Do not add actual personal land records to the repository.

## Project structure

```text
jomicheck_lite/
├── app.py                 # Streamlit interface
├── data_logic.py          # Search and warning rules
├── requirements.txt       # Streamlit dependency
├── data/
│   └── plots.json         # Fictional demonstration records
├── tests/
│   └── test_data_logic.py # Automated tests
├── .streamlit/
│   └── config.toml        # Theme settings
├── .gitignore
└── README.md
```

## Beginner explanation

- **`data/plots.json`** is the small sample dataset. Each object represents a deed record, and each contains an ownership-history list.
- **`data_logic.py`** reads the JSON, searches by IDs, and applies ordinary `if` statements to find review flags.
- **`app.py`** builds the browser interface with Streamlit widgets, metrics, tables and warning messages.
- **`tests/test_data_logic.py`** verifies important cases so changes don't silently break the demo.

## AI use disclosure template

If you used an AI coding assistant while building this project, disclose it in your submission README. Edit this sentence to match your actual use:

> AI coding assistant used for scaffolding and debugging. The team reviewed and tested the application and is responsible for understanding the submitted code.

## Scope and limitations

The rules are illustrative, not legal or fraud-detection determinations. The app searches only the local fictional dataset and cannot independently verify ownership, title, civil cases, mutation, khas/acquisition status, or the authenticity of any real document. A production system would require authorized data access, legal and security review, and official integration.
