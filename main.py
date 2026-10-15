"""
A deliberately small web app for teaching Docker.

It prints things that make the container VISIBLE to students:
  - the hostname, which is the container ID
  - an environment variable, so you can demo  -e
  - a visit counter held in memory, which resets when the container restarts
"""
import os
import socket
import sys
from datetime import datetime

from flask import Flask, jsonify

app = Flask(__name__)

visits = 0
started = datetime.now().strftime("%H:%M:%S")

PAGE = """<!doctype html>
<html><head><meta charset="utf-8"><title>Docker demo</title>
<style>
  body{{font-family:system-ui,-apple-system,sans-serif;background:#16191f;color:#eee;
       display:flex;min-height:100vh;align-items:center;justify-content:center;margin:0}}
  .card{{background:#1f242c;border:1px solid #2e3540;border-radius:10px;padding:34px 40px;
         min-width:380px;box-shadow:0 10px 40px rgba(0,0,0,.4)}}
  h1{{margin:0 0 4px;font-size:21px}}
  p.sub{{margin:0 0 22px;color:#8b94a3;font-size:13px}}
  dl{{display:grid;grid-template-columns:auto 1fr;gap:9px 20px;margin:0;font-size:14px}}
  dt{{color:#8b94a3}}
  dd{{margin:0;font-family:ui-monospace,Menlo,monospace;color:#7fd1b9}}
  .big{{font-size:26px;color:#f0a868}}
</style></head>
<body><div class="card">
  <h1>{greeting}</h1>
  <p class="sub">This page is being served from inside a container.</p>
  <dl>
    <dt>Container ID</dt><dd>{host}</dd>
    <dt>Python</dt><dd>{py}</dd>
    <dt>Started at</dt><dd>{started}</dd>
    <dt>Visits</dt><dd class="big">{visits}</dd>
  </dl>
</div></body></html>"""


@app.route("/")
def home():
    global visits
    visits += 1
    return PAGE.format(
        greeting=os.environ.get("GREETING", "Hello from Docker"),
        host=socket.gethostname(),
        py=sys.version.split()[0],
        started=started,
        visits=visits,
    )


@app.route("/health")
def health():
    return jsonify(status="ok", container=socket.gethostname(), visits=visits)

@app.route("/api/info")
def app_info():
    return jsonify(
        app_name="Docker Demo App",
        python_version=sys.version.split()[0],
        container_id=socket.gethostname(),
        status="running"
    )


if __name__ == "__main__":
    # 0.0.0.0 matters: inside a container, 127.0.0.1 is only reachable
    # from within the container itself, so -p would appear to do nothing.
    app.run(host="0.0.0.0", port=8080)
