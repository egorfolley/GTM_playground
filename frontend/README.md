# Growth Goaled Frontend

React UI for the GTM planner. It expects the Python FastAPI API in `../api.py`.

## Run

From the repo root:

```bash
uvicorn api:app --reload --port 8000
```

From this folder:

```bash
npm install
npm run dev
```

The frontend posts to `/api/build-gtm`. In development, configure Vite to proxy that path to the Python API.
