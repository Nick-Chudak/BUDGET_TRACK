# Personal Budget Tracker

A comprehensive personal budgeting application that combines data analytics, machine learning, and modern software architecture to provide intelligent financial management

## Features

- Transaction import from Excel spreadsheets
- Automatic transaction classification using rule-based and ML approaches
- Cross-platform support (Web and Desktop)
- User authentication and data security
- Intelligent categorization of transactions
- Data visualization and analytics

## Architecture

The application is built with a modular architecture:

- **Backend**: FastAPI (Web) and PyQt6 (Desktop)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **ML Pipeline**: Scikit-learn based classification
- **Frontend**: React (Web) and PyQt6 (Desktop)

## Project Structure

```
budget_track/
├── app/
│   ├── api/            # FastAPI routes and endpoints
│   ├── core/           # Core application logic
│   ├── db/             # Database models and migrations
│   ├── ml/             # ML pipeline and models
│   ├── schemas/        # Pydantic models
│   └── services/       # Business logic services
├── desktop/            # PyQt6 desktop application
├── web/               # React web application
├── tests/             # Test suite
└── scripts/           # Utility scripts
```

## Setup

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
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Initialize the database:
   ```bash
   python scripts/init_db.py
   ```

## Development

- Backend API: `uvicorn app.main:app --reload`
- Desktop App: `python desktop/main.py`
- Web Frontend: `cd web && npm start`

## Testing

```bash
pytest
```

## License