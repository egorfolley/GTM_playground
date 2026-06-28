# AI GTM | Mini-project DEMO

Simple GTM plan generator.

## Quick start

1. Backend

   - Create a Python virtualenv and activate it.
   - pip install -r requirements.txt
   - Export your Anthropic API key: `export ANTHROPIC_API_KEY=your_key_here`
   - Run: `uvicorn backend.app.main:app --reload --port 8000`
2. Frontend

   - cd frontend
   - npm install
   - npm run dev
   - Open http://localhost:5173

## API

- POST /api/build-gtm
  - Body: `{ "founderText": "https://acme.com - ACV $18K - 60-day cycle - $1.2M ARR" }`
  - Returns: GTM plan JSON and `snapshot` text.
- GET /api/health
  - Returns `{ "ok": true }`

## Notes

- Agents call Anthropic directly; no LangChain/LangGraph used.
- Not production-ready: add tests, logging, input validation, and CI before deploying.
