import webbrowser
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/get_data', methods=['GET'])
def get_data():
    return jsonify(message="Hello from Server.py!")

if __name__ == "__main__":
    url = "http://127.0.0.1:8080/get_data"
    webbrowser.open(url, new=2)  # new=2 betyr å åpne i en ny tab, hvis mulig
    app.run(debug=True, host='0.0.0.0', port=8080)
