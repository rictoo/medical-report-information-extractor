#!/usr/bin/env python3
"""
Serve the current directory over HTTPS on port 3005
Compatible with Python 3.7 – 3.13+
"""
import http.server
import ssl
from pathlib import Path

PORT = 3005
CERT = "cert.pem"
KEY  = "key.pem"

# ---------- 1. Ensure cert & key exist ----------
if not (Path(CERT).exists() and Path(KEY).exists()):
    raise SystemExit(
        f"Generate a cert first, e.g.:\n"
        f"  openssl req -x509 -newkey rsa:2048 -nodes "
        f"-keyout {KEY} -out {CERT} -days 365 "
        f"-subj \"/CN=localhost\""
    )

# ---------- 2. Build an HTTPS server ----------
handler = http.server.SimpleHTTPRequestHandler
httpd   = http.server.HTTPServer(("", PORT), handler)

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)     # future-proof default
context.load_cert_chain(certfile=CERT, keyfile=KEY)

# Wrap the *listening* socket once, before serve_forever()
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print(f"Serving HTTPS on https://localhost:{PORT}  (Ctrl-C to stop)")
httpd.serve_forever()
