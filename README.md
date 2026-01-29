# Webhook Repo

A simple Python Full-stack application to receive, store, and display GitHub webhook events (push, pull request, merge) using Flask, MongoDB, and a minimal JavaScript frontend.

## Features
- Receives GitHub webhook events (push, pull request, merge)
- Stores event data in MongoDB
- REST API to fetch recent events
- Frontend to display latest repository activity

## Project Structure
```
backend/
  app.py            # Flask API server
  db.py             # MongoDB connection setup
  models.py         # Event formatting utilities
  requirements.txt  # Python dependencies
  .env              # Environment variables (MongoDB URI, DB name)
frontend/
  index.html        # Main UI
  script.js         # Fetches and displays events
  style.css         # Basic styling
```

## Backend (Flask API)
- **/webhook** (`POST`): Receives GitHub webhook events. Supports push, pull request, and merge events. Stores formatted event data in MongoDB.
- **/events** (`GET`): Returns the 20 most recent events, sorted by timestamp (latest first).

### Environment Variables
Set in `backend/.env`:
- `MONGO_URI`: MongoDB connection string
- `DB_NAME`: Database name

### Running the Backend
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the server:
   ```bash
   python app.py
   ```
   The API will run on `http://localhost:5000`.

## Frontend
- Fetches and displays the latest events from the backend API.
- Auto-refreshes every 15 seconds.

### Running the Frontend
Just open `frontend/index.html` in your browser.

## Setting Up GitHub Webhooks
1. Deploy or run the backend server so it is accessible from GitHub (use a tool like [ngrok](https://ngrok.com/) for local development).
2. In your GitHub repository, go to **Settings > Webhooks > Add webhook**.
3. Set the Payload URL to your backend's `/webhook` endpoint (e.g., `http://<your-server>/webhook`).
4. Choose content type `application/json`.
5. Select events: push, pull request, etc.
6. Save the webhook.

## Requirements
- Python 3.8+
- MongoDB (local or Atlas)
- Flask, pymongo, flask-cors, python-dotenv
