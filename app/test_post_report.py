import requests
import json

# Replace with your actual Flask server address
url = "http://127.0.0.1:5000/analysis-reports/"

# Prepare dummy data (match your model’s expected feature shape)
payload = {
    "features": [0.1] * 247,  # This must be your exact ML feature length (e.g. 247 values)
    "rhythm_analysis": "Normal baseline",
    "anomalies": "No epileptic discharge",
    "state_id": 1,
    "eeg_id": 2
}

# Make the POST request
response = requests.post(url, data=json.dumps(payload), headers={"Content-Type": "application/json"})

# Show the result
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
