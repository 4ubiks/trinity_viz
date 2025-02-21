import json

def load_preferences():
    with open("preferences.json", "r") as file:
        return json.load(file)

preferences = load_preferences()
rtsp_url = preferences.get("rtsp_url")
