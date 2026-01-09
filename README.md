# A guide to UConn SSO by HQG

This repository contains a Python Flask server that integrates UConn SSO and returns the authenticated user's UConn NetId.

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

## Code Explanation

{to be completed}

Example response from UConn CAS server:
```xml
<cas:serviceResponse xmlns:cas='http://www.yale.edu/tp/cas'>
    <cas:authenticationSuccess>
        <cas:user>abc12345</cas:user>
        
    </cas:authenticationSuccess>
</cas:serviceResponse>
```