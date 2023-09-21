# Import 'webbrowser' for interacting with web browsers.
import webbrowser
# Import 'Flask' for setting up the server, and 'jsonify' for creating JSON responses.
from flask import Flask, jsonify

# Initialize a Flask application.
app = Flask(__name__)

# Define a route that returns a JSON response.
@app.route('/get_data', methods=['GET'])
def get_data():
    return jsonify(message="Hello from Server.py!")

# Run the server and open the browser if this script is the main module.
if __name__ == "__main__":
    url = "http://127.0.0.1:8080/get_data"
    webbrowser.open(url, new=2)  # Open URL in a new tab, if possible.
    app.run(debug=True, host='0.0.0.0', port=8080)  # Start the Flask app with specified settings.
