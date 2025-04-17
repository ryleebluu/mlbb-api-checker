
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/validate', methods=['POST'])
def validate():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    token = data.get('game_token')

    if not email or not password or not token:
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json"
    }

    payload = {
        "email": email,
        "password": password,
        "token": token,
        "platform_type": "moonton"
    }

    try:
        response = requests.post("https://accountmtapi.mobilelegends.com/api/user/login", json=payload, headers=headers)

        if response.status_code == 200:
            return jsonify({"status": "valid", "message": "Account is valid", "email": email})
        else:
            return jsonify({"status": "invalid", "message": "Invalid credentials or token", "email": email})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
