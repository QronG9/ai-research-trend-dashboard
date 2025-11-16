AI-Trend: Cloud Function + Vercel Frontend

Overview
- Backendless architecture
- Cloud Function pulls OpenAlex, aggregates counts, and writes static JSON to GCS bucket ai-trend-cache
- Frontend fetches JSON directly from GCS and triggers refresh by POSTing to the Cloud Function URL

Folders
- cloud-function/: deployable Google Cloud Function (Python)
- frontend/: app updated to fetch from GCS and trigger Cloud Function
- frontend-vercel/: standalone copy of frontend, ready for GitHub + Vercel

Cloud Function
1) Prereqs
- gcloud CLI authenticated and project set
- Enable Cloud Functions and Cloud Storage APIs
- Ensure bucket ai-trend-cache exists and is publicly readable (Storage Object Viewer on objects)

2) Deploy

gcloud functions deploy ai_trend_refresh \
--runtime python311 \
--trigger-http \
--allow-unauthenticated \
--region europe-west1 \
--source cloud-function

3) Test
- Note the HTTPS URL output by gcloud. Example: https://europe-west1-<project>.cloudfunctions.net/ai_trend_refresh
- Trigger a refresh:
  curl -X POST "https://europe-west1-<project>.cloudfunctions.net/ai_trend_refresh"
- Inspect GCS bucket for files like: natural_language_processing_2010_2025.json

Frontend (Vercel)
1) Configure
- In Vercel Project Settings -> Environment Variables, set VITE_CLOUD_FUNCTION_URL to the Cloud Function URL

2) Deploy
- From frontend-vercel/ directory run:
  vercel --prod

3) Behavior
- Refresh button POSTs to Cloud Function URL
- UI fetches JSON from https://storage.googleapis.com/ai-trend-cache/{slug}_2010_2025.json

Local Dev
- You can still run `npm run dev` in frontend/ (or frontend-vercel/) to preview the static UI
- The refresh action will no-op unless VITE_CLOUD_FUNCTION_URL is set

Notes
- Direction slugs in frontend are derived by lowercasing and replacing spaces/"/" with underscore; e.g. "Natural Language Processing" -> natural_language_processing
- Cloud Function writes exactly {slug}_2010_2025.json files.
