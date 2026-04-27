from garminconnect import Garmin
from flask import Flask, jsonify
from datetime import date, timedelta
import os

app = Flask(__name__)

email = os.environ.get("GARMIN_EMAIL")
password = os.environ.get("GARMIN_PASSWORD")

@app.route("/")
def index():
    return "Garmin-morgen kjører!"

@app.route("/data")
def get_data():
    try:
        client = Garmin(email, password)
        client.login()
        today = date.today().isoformat()
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        stats = client.get_stats(today)
        sleep = client.get_sleep_data(yesterday)
        activities = client.get_activities(0, 7)
        return jsonify({
            "date": today,
            "steps": stats.get("totalSteps"),
            "body_battery": stats.get("bodyBatteryMostRecentValue"),
            "resting_hr": stats.get("restingHeartRate"),
            "sleep_score": sleep.get("dailySleepDTO", {}).get("sleepScores", {}).get("overall", {}).get("value"),
            "recent_activities": [
                {
                    "name": a.get("activityName"),
                    "date": a.get("startTimeLocal"),
                    "duration_min": round(a.get("duration", 0) / 60),
                    "avg_hr": a.get("averageHR")
                }
                for a in activities[:7]
            ]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
