import os
import secrets
import hashlib
import base64
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("SALESFORCE_CLIENT_ID")
CLIENT_SECRET = os.getenv("SALESFORCE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SALESFORCE_REDIRECT_URI")
LOGIN_URL = os.getenv("SALESFORCE_LOGIN_URL")

# Temporary storage for OAuth state and PKCE verifier
oauth_store = {}


def generate_pkce():
    code_verifier = secrets.token_urlsafe(64)

    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode("utf-8")).digest()
    ).rstrip(b"=").decode("utf-8")

    return code_verifier, code_challenge


def get_salesforce_authorization_url():
    state = secrets.token_urlsafe(32)

    code_verifier, code_challenge = generate_pkce()

    # Save verifier temporarily.
    oauth_store[state] = code_verifier

    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }

    return (
        f"{LOGIN_URL}/services/oauth2/authorize?"
        f"{urlencode(params)}"
    )


def exchange_code_for_token(code, state):
    code_verifier = oauth_store.pop(state, None)

    if not code_verifier:
        raise ValueError("Invalid or expired OAuth state")

    token_url = f"{LOGIN_URL}/services/oauth2/token"

    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code": code,
        "code_verifier": code_verifier,
    }

    response = requests.post(token_url, data=data)

    if response.status_code != 200:
        raise Exception(
            f"Salesforce token error: {response.text}"
        )

    return response.json()