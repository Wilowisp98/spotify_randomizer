import base64
import hashlib
import requests
import secrets
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class SpotifyAuth:
    def __init__(self, client_id, scope):
        self.client_id = client_id
        self.scope = scope
        self.redirect_uri = 'http://localhost:8080'
        self.token_url = 'https://accounts.spotify.com/api/token'
        self.auth_url = 'https://accounts.spotify.com/authorize'
        self.access_token = None
        self.auth_code = None
        self.server = None

    def generate_code_verifier(self):
        return secrets.token_urlsafe(64)[:128]

    def generate_code_challenge(self, code_verifier):
        sha256 = hashlib.sha256(code_verifier.encode('utf-8')).digest()
        return base64.urlsafe_b64encode(sha256).decode('utf-8').rstrip('=')

    def get_auth_code(self, code_challenge):
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'code_challenge_method': 'S256',
            'code_challenge': code_challenge,
            'scope': self.scope,
        }
        auth_url = requests.Request('GET', self.auth_url, params=params).prepare().url
        print(f"Opening browser for authorization...")
        webbrowser.open(auth_url)

        self.server = HTTPServer(('localhost', 8080), self.CallbackHandler)
        self.server.auth_instance = self
        self.server.timeout = 60

        print("Waiting for authorization (timeout in 60 seconds)...")
        self.server.handle_request()

        if not self.auth_code:
            raise Exception("Failed to get authorization code. Please check if the browser opened and if you authorized the application.")
        return self.auth_code

    class CallbackHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            query_components = parse_qs(urlparse(self.path).query)
            if 'code' in query_components:
                self.server.auth_instance.auth_code = query_components['code'][0]
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"Authorization successful! You can close this window.")
            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"Authorization failed.")

        def log_message(self, format, *args):
            # Suppress console output
            return

    def get_tokens(self, auth_code, code_verifier):
        data = {
            'client_id': self.client_id,
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': self.redirect_uri,
            'code_verifier': code_verifier,
        }
        response = requests.post(self.token_url, data=data)
        response.raise_for_status()
        return response.json()

    def authorize(self):
        try:
            code_verifier = self.generate_code_verifier()
            code_challenge = self.generate_code_challenge(code_verifier)
            auth_code = self.get_auth_code(code_challenge)
            tokens = self.get_tokens(auth_code, code_verifier)
            self.access_token = tokens['access_token']
            return self.access_token
        except Exception as e:
            print(f"Authorization failed: {str(e)}")
            print("Please ensure that:")
            print("1. Your Spotify app's redirect URI is set to http://localhost:8080 in the Spotify Developer Dashboard")
            print("2. You're using the correct client ID")
            print("3. You have a stable internet connection")
            print("4. You authorized the application in the browser window that opened")
            raise