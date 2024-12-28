from flask import Flask, request, jsonify
import os
from datetime import datetime
import garth

app = Flask(__name__)

# Helper function to configure Garth and retrieve data
def get_data(email, password, period=28):
    garth.login(email, password)
    garth.save(os.path.expanduser("~/.garth"))
    garth.configure(domain="garmin.com")
    
    # Fetch data
    sleep_summary = garth.DailySleep.list(period=period)
    stress_summary=garth.DailyStress.list(period=period)
    hrv_summary=garth.DailyHRV.list(period=period)
    steps_summary=garth.DailySteps.list(period=period)
    intensity_mins_summary=garth.DailyIntensityMinutes.list(period=period)
    
    return {
        "sleep": {"summary": sleep_summary},
        "hrv": {"summary": hrv_summary},
        "stress": {"summary": stress_summary},
        "steps": {"summary": steps_summary},
        "intensityMins": {"summary": intensity_mins_summary},
    }

# API endpoint to retrieve data
@app.route('/api/data', methods=['POST'])
def api_data():
    # Parse request JSON for credentials and parameters
    req_data = request.get_json()
    email = req_data.get('email')
    password = req_data.get('password')
    period = req_data.get('period', 28)
    
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    
    try:
        data = get_data(email, password, period)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)