from flask import Flask, render_template, request
import requests
from datetime import datetime, timedelta
import pytz
import os

# --- Monitoring ---
from datadog import initialize, api
import bugsnag
from bugsnag.flask import handle_exceptions

# Datadog Init
initialize(api_key=os.getenv("e2530648fc8da01f715fab430d530a25"))

# Bugsnag Init
bugsnag.configure(api_key=os.getenv("f5047dec7c00e161eed20cbb2eb9da0a"), project_root=".")
app = Flask(__name__)
handle_exceptions(app)

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crash')
def crash():
    raise Exception("Intentional Bugsnag error")
