
# Webhook Repo

This is a simple Flask app that receives GitHub webhook events (push, pull request, merge) and saves them to MongoDB.

## What it does
- Receives webhook events from GitHub (push, pull request, merge)
- Stores event details in a MongoDB collection
- Provides a minimal web UI to view the 10 most recent events
- The UI updates automatically every 15 seconds


## How to run
1. Install requirements: `pip install -r requirements.txt`
2. Set up your `.env` file with your MongoDB URI (e.g. `MONGODB_URI=mongodb://localhost:27017/webhook_github`)
3. Start the app: `python app.py`
4. If you want to test GitHub webhooks from your local machine, use [ngrok](https://ngrok.com/):
   - Download and install ngrok
   - Run `ngrok http 5000` in a separate terminal
   - Use the generated public URL as your webhook endpoint in GitHub
5. Open `http://localhost:5000/` in your browser to see the dashboard


