from flask import Flask, request, jsonify
import garminconnect
from datetime import date, timedelta

app = Flask(__name__)

# API endpoint to retrieve data
@app.route('/api/summary', methods=['POST'])
def api_summary():
    # Parse request JSON for credentials and parameters
    req_data = request.get_json()
    email = req_data.get('email')
    password = req_data.get('password')
    period = req_data.get('period', 28)
    
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    
    try:
        garmin = garminconnect.Garmin(email, password)
        garmin.login()
        
        data = []

        for x in range(period):
            d = (date.today() - timedelta(days=x)).isoformat()
            data.append(garmin.get_stats_and_body(d))
        
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)