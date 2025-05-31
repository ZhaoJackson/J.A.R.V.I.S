# J.A.R.V.I.S - Personal Assistant

A comprehensive personal assistant that helps manage health, finance, and daily tasks using AI and automation.

## Features

- Web information fetching using LLM-AXE
- Real-time model processing with Azure API
- Interactive web interface with Streamlit
- Health and finance data management
- n8n workflow integration

## Project Structure

```
J.A.R.V.I.S/
├── app/                    # Main application code
│   ├── api/               # FastAPI backend
│   ├── frontend/          # Streamlit interface
│   ├── models/            # Database models
│   └── services/          # Business logic
├── config/                # Configuration files
├── data/                  # Data storage
├── docs/                  # Documentation
├── scripts/               # Utility scripts
└── tests/                 # Test files
```

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
- Copy `.env.example` to `.env`
- Fill in your Azure API credentials and other configurations

4. Initialize the database:
```bash
python scripts/init_db.py
```

5. Run the application:
```bash
streamlit run app/frontend/main.py
```

## Environment Variables

Create a `.env` file with the following variables:
- AZURE_API_KEY
- AZURE_ENDPOINT
- DATABASE_URL
- N8N_WEBHOOK_URL

## License

MIT License 