from flask import Flask, request
import itertools
import requests

app = Flask(__name__)

# TODO: Add backend server URL for round-robin distribution
# TODO: implement the appropriate, service-aware backend -server URL for the load balancer
# "http://10.244.0.143:5001", "http://10.244.0.142:5001"
BACKEND_SERVERS = [
     "http://flask-backend-service:5001"
]

print(f"Configured backend servers: {BACKEND_SERVERS}")

# Round-robin iterator for distributing requests
server_pool = itertools.cycle(BACKEND_SERVERS)

@app.route('/model-info')
def load_balance():
    print("Received request for /model-info")
    backend_url = next(server_pool)
    response = requests.get(f"{backend_url}/model-info")
    try:
        data = response.json()
    except ValueError:
        return {"error": "Invalid JSON from backend", "raw": response.text}, 502
    return data, response.status_code

@app.route('/predict', methods=['POST'])
def predict():
    print("Received request for /predict")

    backend_url = next(server_pool)
    url = f"{backend_url}/predict"

    # TODO: Implement the rest of the POST request for the predict endpoint
    response = requests.post(url, json=request.get_json())
    try:
        data = response.json()
    except ValueError:
        return {"error": "Invalid JSON from backend", "raw": response.text}, 502
    return data, response.status_code


if __name__ == '__main__':
    # TODO: Change the port if necessary (default is 8080)
    app.run(host='0.0.0.0', port=8080)
