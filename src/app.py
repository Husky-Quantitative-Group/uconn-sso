import os
import urllib.parse
import xml.etree.ElementTree as ET

import requests
from flask import Flask, request, redirect, Response

app = Flask(__name__)

# Configure
CAS_BASE = "https://login.uconn.edu/cas"
SERVICE_URL = "http://localhost:3000/callback"
CAS_NS = {"cas": "http://www.yale.edu/tp/cas"}

def validate_cas_ticket(ticket):
    service_enc = urllib.parse.quote(SERVICE_URL, safe="")
    validate_url = f"{CAS_BASE}/serviceValidate?service={service_enc}&ticket={urllib.parse.quote(ticket, safe='')}"
    r = requests.get(validate_url, timeout=5)
    xml = r.text

    try:
        root = ET.fromstring(xml)
    except ET.ParseError:
        return None

    success = root.find("cas:authenticationSuccess", CAS_NS)
    if success is None:
        return None

    return success.findtext("cas:user", default="", namespaces=CAS_NS) or None

@app.get("/")
def index():
    return (
        "<a href='/login'>Login with UConn CAS</a><br>"
        f"CAS_BASE={CAS_BASE}<br>"
        f"SERVICE_URL={SERVICE_URL}"
    )

@app.get("/login")
def login():
    service = urllib.parse.quote(SERVICE_URL, safe="")
    return redirect(f"{CAS_BASE}/login?service={service}", code=302)

@app.get("/callback")
def callback():
    ticket = request.args.get("ticket")
    if not ticket:
        return Response("Failed", 400)

    netid = validate_cas_ticket(ticket)
    if netid:
        return f"Success!<br>NetID: {netid}"

    return Response("Failed", 401)

@app.get("/logout")
def logout():
    # In a real app, clear your local session first.
    return redirect(f"{CAS_BASE}/logout", code=302)

if __name__ == "__main__":
    # Flask dev server
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "3000")), debug=True)
