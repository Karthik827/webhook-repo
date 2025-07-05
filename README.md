
# Webhook Repo


This is a Flask application that receives GitHub webhook events (push, pull request, merge), stores them in MongoDB, and displays them in a web UI.


## Features
- Receives webhook events from GitHub (push, pull request, merge)
- Stores event details in a MongoDB collection
- Provides a web UI to view the 10 most recent events
- The UI updates automatically every 15 seconds



## How to run
1. Install requirements:
   ```sh
   pip install -r requirements.txt
   ```
2. (Recommended) Set up your `.env` file in the project root with your MongoDB URI:
   ```env
   MONGODB_URI=mongodb://localhost:27017/webhook_github
   ```
   > Note: By default, the URI is hardcoded in `app/extensions.py`. For best practice, update the code to load from `.env` using `python-dotenv`.
3. Start MongoDB (if not already running):
   - On Windows: `net start MongoDB`
   - On Linux/macOS: `sudo systemctl start mongod`
4. Start the app:
   ```sh
   python run.py
   ```
5. (Optional) To test GitHub webhooks from your local machine, use [ngrok](https://ngrok.com/):
   - Download and install ngrok
   - Run `ngrok http 5000` in a separate terminal
   - Use the generated public URL as your webhook endpoint in GitHub
6. Open `http://localhost:5000/` in your browser to see the dashboard


## API Endpoints

- `POST /webhook/receiver` — Receives GitHub webhook events
- `GET /webhook/events` — Returns the 10 most recent events (JSON)
- `GET /` — Web UI dashboard

## Requirements

- Flask
- pymongo
- python-dotenv
- python-dateutil

See `requirements.txt` for exact versions.





