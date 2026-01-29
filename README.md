# Flask+Webhook

## Overview
A production-ready Flask app to receive GitHub webhook events, store them in MongoDB, and display them in a minimal UI.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up MongoDB (local or cloud) and set `MONGO_URI` env variable if not using default.
3. Run the app:
   ```bash
   python app.py
   ```
4. Configure your GitHub repo webhook to POST to `/webhook` endpoint.

## UI
- Open `http://localhost:5000` to view the live feed.

## Notes
- The UI polls `/events` every 15 seconds for updates.
- Only minimal, necessary data is shown.
