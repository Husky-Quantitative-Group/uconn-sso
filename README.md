# A guide to UConn SSO by HQG

This repository contains a Python Flask server that integrates UConn Single Sign-On (SSO) and returns the authenticated user's UConn NetId.

Click [here](https://iam.uconn.edu/the-cas-protocol-for-application-owners/) to view a more in-depth explanation of how the CAS protocol works, made by UConn IT Services.

---

## Testing Locally

To spin up the Flask server on your local machine, follow these steps.

### 1. Clone and enter the repository
```bash
git clone https://github.com/Husky-Quantitative-Group/uconn-sso.git
cd uconn-sso
```

### 2. Run the server
```bash
python3 -m venv .venv && source .venv/bin/activate # optional, but recommended
pip install -r src/requirements.txt
python src/app.py # or python3 if not using virtual environment
```

### 3. Open in browser

The Flask server and frontend should be available on `http://localhost:3000`

---

## Step-by-Step Flow

This app implements the basic UConn CAS single sign-on flow, using the hardcoded CAS base (`https://login.uconn.edu/cas`) and callback URL (`http://localhost:3000/callback`) in `src/app.py`:

1. `/login` sends the user to `https://login.uconn.edu/cas/login` with `service=http://localhost:3000/callback`.
2. After login, CAS redirects to `/callback` with a short-lived `ticket` query param.
3. `/callback` calls `https://login.uconn.edu/cas/serviceValidate` with the same `service` and the `ticket`.
4. CAS returns XML with either `authenticationSuccess` (including the NetID) or `authenticationFailure`.
5. On success, your app should create its own session and treat the user as logged in (not implemented here).

Example response from CAS server `/serviceValidate` endpoint:
```xml
<cas:serviceResponse xmlns:cas='http://www.yale.edu/tp/cas'>
    <cas:authenticationSuccess>
        <cas:user>abc12345</cas:user>
        
    </cas:authenticationSuccess>
</cas:serviceResponse>
```
