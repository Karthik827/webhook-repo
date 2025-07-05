"""
Flask application to receive GitHub webhook events, store them in MongoDB, and display in a UI.
Handles push, pull request, and merge events for the Developer Assessment Task.
Author: Karthik827
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)