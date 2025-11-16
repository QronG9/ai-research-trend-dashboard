# 📈 OpenAlex AI Trend Explorer (Cloud-Native Edition)

[![GitHub Stars](https://img.shields.io/github/stars/QronG9/ai-research-trend-dashboard?style=social)](https://github.com/QronG9/ai-research-trend-dashboard)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Tech Stack](https://img.shields.io/badge/Frontend-React%2FVite%2FFirebase-blue)](https://vitejs.dev/)
[![Tech Stack](https://img.shields.io/badge/Backend-CloudFunction%2FGCS%2FPython-green)](https://cloud.google.com/functions)

---

## 🚀 Live Dashboard & Project Overview

This is a real-time visualization tool that tracks the publication volume trends of over 30 AI research subfields sourced from the **OpenAlex** API (2010–2025).

**Live Demo URL (立即访问):** [https://ai-trend-478401.web.app](https://ai-trend-478401.web.app)

**Key Features:**
* **Backendless Architecture:** Migrated from FastAPI to Google Cloud Functions (GCP) + Firebase Hosting.
* **Static Data Hosting:** Frontend fetches data directly from Google Cloud Storage (GCS) for lightning-fast load times.
* **On-Demand Updates:** Users can trigger data recalculation using the "Refresh" button.
* **Visualizations:** Provides Trend Line Charts, Rankings, and Heatmaps.



---

## 🧠 Project Architecture (Monorepo Structure)

This repository follows a Monorepo structure, containing distinct components for the compute pipeline and the frontend application.

### 1. Compute Pipeline (Cloud Function)

| Folder | Description | Deployed To | Role |
| :--- | :--- | :--- | :--- |
| `cloud-function/` | Contains all Python source (`main.py`, `openalex_client.py`). | **Google Cloud Functions** | Fetches data from OpenAlex, aggregates, and writes to GCS. |
| `cache/` | Stores the final generated JSON files (`{slug}_2010_2025.json`). | **Google Cloud Storage (GCS)** | Public data source for the frontend. |

### 2. Frontend Application

| Folder | Description | Deployed To | Role |
| :--- | :--- | :--- | :--- |
| `frontend-vercel/` | The core React/Vite source code. | **Firebase Hosting** | Reads JSON from GCS and provides the user interface. |

---

## 🛠️ Installation & Deployment

This project requires Python (for the backend code) and Node.js (for the frontend).

### Local Setup (Python & Backend Code)

1.  **Environment:** Create a virtual environment and activate it.
    ```bash
    python -m venv trend-env
    source trend-env/bin/activate  # Or trend-env\Scripts\activate on Windows
    ```
2.  **Dependencies:** Install backend analysis dependencies.
    ```bash
    pip install -r requirements.txt
    ```

### Production Deployment (GCP & Firebase)

The full deployment involves deploying the Cloud Function (Python) and the Frontend (React).

1.  **Cloud Function Deploy:** (Refer to `README_DEPLOY.md` for specific commands.)
2.  **Frontend Deploy:** Built from the `frontend-vercel/` directory and deployed to Firebase Hosting.

---

## 💡 Usage (Python Scripts)

The repository still contains the original scripts and notebooks for local data processing:

* **Full Pipeline:** `python run_all_directions.py` (Writes all caches and CSV output).
* **Demo Notebook:** `jupyter notebook notebooks/nlp_trend_demo.ipynb`

***
