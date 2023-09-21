from flask import Flask, jsonify
import requests

app = Flask(__name__)

BASE_URL = "http://192.168.0.1:80"

def get_service_version():
    """
    Makes a GET request to the service to obtain its version.
    
    :return: A string representing the service version or None if an error occurs.
    """
    try:
        response = requests.get(f"{BASE_URL}/version", timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        app.logger.error(f"Error fetching service version: {e}")
        return None

@app.route('/local_version', methods=['GET'])
def obtain_service_version():
    """
    Handles the GET requests to the '/local_version' route.
    
    :return: A JSON object containing the service version message 
             and a corresponding HTTP status code.
    """
    version = get_service_version()
    if version:
        return jsonify(message=f"Service Version: {version}")
    else:
        return jsonify(message="Failed to get service version."), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
