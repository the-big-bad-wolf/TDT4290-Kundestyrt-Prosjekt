import webbrowser
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/get_data', methods=['GET', 'POST'])
def get_data():
    if request.method == 'POST':
        direction = request.json.get('direction', '')
        if direction == "up":
            return jsonify(response="Ping received! Direction is UP!")
        else:
            return jsonify(response="Direction is not UP!")
    return jsonify(message="Hello from Server.py!")

if __name__ == "__main__":
    url = "http://127.0.0.1:8080/get_data"
    webbrowser.open(url, new=2)
    app.run(debug=True, host='0.0.0.0', port=8080)
