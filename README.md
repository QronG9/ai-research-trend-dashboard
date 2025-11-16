# OpenAlex AI Trend Explorer

A minimal, beginner-friendly project that fetches AI-related bibliometric data from the OpenAlex API and provides:
- Python scripts + notebooks for analysis
- A FastAPI backend
- A React-based dashboard

## Project Overview
- Fetches counts per year using fast `group_by=publication_year` queries.
- 30 AI sub-directions defined in `src/config/directions.py`.
- Caches per-direction results to `cache/`.
- Outputs a long-format CSV at `output/ai_directions_counts.csv`.
- Provides line charts and heatmaps via scripts, notebooks, and a web dashboard.

## Installation
1) Create and activate a virtual environment (Windows example):

```
python -m venv trend-env
trend-env\Scripts\activate
```

2) Install dependencies:

```
pip install -r requirements.txt
```

Note: In VS Code, ensure the interpreter is set to `E:\\trend\\trend-env\\Scripts\\python.exe`.

## Usage (Python)
- Run the full 30-direction pipeline (writes CSV and heatmap):

```
python run_all_directions.py
```

- Run the simple NLP trend demo:

```
python demo_nlp_trend.py
```

- Open the notebook and run the cells:

```
jupyter notebook notebooks/nlp_trend_demo.ipynb
```

### Web Dashboard
This repo includes a small FastAPI backend and a React dashboard.

Backend (FastAPI):

```
trend-env\Scripts\activate
uvicorn src.frontend_api.server:app --reload
```

Frontend (React + Vite):

```
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

Dashboard Panels:
- Trend line chart: select a direction and view counts (2010–2025)
- Rankings: latest year’s top directions as a bar chart
- Heatmap: directions × years

Refresh Button:
- Triggers POST /api/refresh to run `run_all_directions.py`, recomputing caches and CSV.
- The dashboard auto-updates after completion.

## Notes
- OpenAlex is free and does not require an API key.
- Counts are approximate and depend on filters (concept id preferred; keyword fallback may double-count overlaps).
- The demo uses small ranges in some scripts for quick runs.
