from flask import Flask, request, jsonify
import garminconnect
from datetime import date, timedelta

app = Flask(__name__)

def login_and_get_client():
    # Parse request JSON for credentials and parameters
    req_data = request.get_json()
    email = req_data.get('email')
    password = req_data.get('password')
    
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    
    try:
        garmin = garminconnect.Garmin(email, password)
        garmin.login()
        
        return garmin
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/summary', methods=['POST'])
def api_summary():
    req_data = request.get_json()
    period = req_data.get('period', 30)
    
    try:
        garmin = login_and_get_client();
        data = []

        for x in range(period+1):
            d = (date.today() - timedelta(days=x)).isoformat()
            data.append(garmin.get_stats_and_body(d))
        
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/activities', methods=['POST'])
def api_activities():
    req_data = request.get_json()
    period = req_data.get('period', 30)
    
    try:
        garmin = login_and_get_client();
        data = garmin.get_activities_by_date(date.today() - timedelta(period), date.today())
        
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/privacy', methods=['GET'])
def privacy():
    return "There is none!"

if __name__ == '__main__':
    app.run(debug=True)