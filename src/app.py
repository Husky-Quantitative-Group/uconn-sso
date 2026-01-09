import os
import urllib.parse
import xml.etree.ElementTree as ET

import requests
from flask import Flask, request, redirect, Response

app = Flask(__name__)

# Configure
CAS_BASE = "https://login.uconn.edu/cas"
SERVICE_URL = "http://localhost:3000/callback"

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
        return Response("Missing ?ticket", 400)

    service_enc = urllib.parse.quote(SERVICE_URL, safe="")
    validate_url = f"{CAS_BASE}/serviceValidate?service={service_enc}&ticket={urllib.parse.quote(ticket, safe='')}"
    r = requests.get(validate_url, timeout=5)
    xml = r.text

    print(xml)

    # Parse minimal CAS v2 response
    ns = {"cas": "http://www.yale.edu/tp/cas"}
    try:
        root = ET.fromstring(xml)
        success = root.find("cas:authenticationSuccess", ns)
        if success is not None:
            user = success.findtext("cas:user", default="", namespaces=ns)
            attrs = success.find("cas:attributes", ns)
            # Build a simple attributes dict if present
            attr_lines = []
            if attrs is not None:
                for child in list(attrs):
                    tag = child.tag.split("}", 1)[-1]  # strip namespace
                    attr_lines.append(f"{tag}: {child.text}")
            attr_block = "<br>".join(attr_lines) if attr_lines else "(no attributes)"

            # Here is where you'd create your own app session.
            return (
                f"<h3>authenticationSuccess</h3>"
                f"<b>user:</b> {user}<br>"
                f"<b>attributes:</b><br>{attr_block}<br><br>"
                f"<code>serviceValidate:</code><pre>{xml}</pre>"
            )
        else:
            failure = root.find("cas:authenticationFailure", ns)
            if failure is not None:
                code = failure.attrib.get("code", "UNKNOWN")
                msg = failure.text or ""
                return (
                    f"<h3>authenticationFailure</h3>"
                    f"<b>code:</b> {code}<br>"
                    f"<b>message:</b> {msg}<br><br>"
                    f"<code>serviceValidate:</code><pre>{xml}</pre>", 401
                )
            # Unknown response
            return f"<h3>Unknown CAS response</h3><pre>{xml}</pre>", 502
    except ET.ParseError:
        return f"<h3>Non-XML CAS response</h3><pre>{xml}</pre>", 502

@app.get("/logout")
def logout():
    # In a real app, clear your local session first.
    return redirect(f"{CAS_BASE}/logout", code=302)

if __name__ == "__main__":
    # Flask dev server
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "3000")), debug=True)
