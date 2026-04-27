from garminconnect import Garmin
from datetime import date, timedelta
import json
import os

email = os.environ.get("GARMIN_EMAIL")
password = os.environ.get("GARMIN_PASSWORD")

def get_garmin_data():
    client = Garmin(email, password)
    client.login()
    
    today = date.today().isoformat()
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    
    stats = client.get_stats(today)
    sleep = client.get_sleep_data(yesterday)
    activities = client.get_activities(0, 7)
    hrv = client.get_hrv_data(today)
    training_readiness = client.get_training_readiness(today)
    
    return {
        "date": today,
        "steps": stats.get("totalSteps"),
        "body_battery": stats.get("bodyBatteryMostRecentValue"),
        "resting_hr": stats.get("restingHeartRate"),
        "​​​​​​​​​​​​​​​​
