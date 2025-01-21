from flask import Flask, redirect, url_for, session, request, render_template_string, render_template
from oauthlib.oauth2 import WebApplicationClient
import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


app = Flask(__name__)
app.secret_key = "mysecret"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_DISCOVERY_URL = os.getenv('GOOGLE_DISCOVERY_URL')
REDIRECT_URI = os.getenv('REDIRECT_URI')

client = WebApplicationClient(GOOGLE_CLIENT_ID)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@app.route("/")
def index():
    if "user" in session:
        return render_template("index.html", user=session["user"])
    return render_template("index.html", user=None)

@app.route("/login")
def login():
    # Get Google's authorization endpoint
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

  
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=REDIRECT_URI,
        scope=["openid", "email", "profile", "https://www.googleapis.com/auth/calendar.readonly"],
        state = "/events"
    )
    return redirect(request_uri)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    state = request.args.get("state")  

   
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]


    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=REDIRECT_URI,
        code=code,
        client_secret=GOOGLE_CLIENT_SECRET,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    
    token_data = token_response.json()
    client.parse_request_body_response(json.dumps(token_data))

  
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

 
    userinfo = userinfo_response.json()
    session["user"] = {
        "id": userinfo["sub"],
        "email": userinfo["email"],
        "name": userinfo["name"],
        "picture": userinfo["picture"],
        "access_token": token_data.get("access_token") 
    }

   
    return redirect(state or url_for("index"))


@app.route("/events")
def events():
    if "user" not in session:
        return redirect(url_for("index"))
    
   
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    
  
    if not start_date:
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + "Z"
    else:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + "Z"
    
    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d").replace(hour=23, minute=59, second=59, microsecond=0).isoformat() + "Z"
    

    access_token = session["user"]["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "orderBy": "startTime",
        "singleEvents": True,
        "maxResults": 100,
        "timeMin": start_date,
    }
    if end_date:
        params["timeMax"] = end_date
    
    events_response = requests.get(
        "https://www.googleapis.com/calendar/v3/calendars/primary/events",
        headers=headers,
        params=params,
    )
    
    events = events_response.json().get("items", [])
   
    events.sort(key=lambda x: x["start"].get("dateTime", x["start"].get("date")), reverse=True)
    
    return render_template('events.html', events=events)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, host = '0.0.0.0', port = 5000)
