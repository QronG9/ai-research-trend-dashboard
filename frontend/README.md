# AI Research Trend Dashboard (Frontend)

A minimal React + Vite dashboard that connects to the FastAPI backend to display AI research trends from OpenAlex.

## Setup

1) Install dependencies:

```
npm install
```

2) Run the dev server:

```
npm run dev
```

The app defaults to calling the API at http://localhost:8000.
You can customize by setting VITE_API_BASE in an .env file, e.g.:

```
VITE_API_BASE=http://localhost:8000
```

Open the app at http://localhost:5173 (default Vite port).
