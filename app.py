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
initialize(api_key=os.getenv("DATADOG_API_KEY"))

# Bugsnag Init
bugsnag.configure(api_key=os.getenv("BUGSNAG_API_KEY"), project_root=".")
app = Flask(__name__)
handle_exceptions(app)

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crash')
def crash():
    raise Exception("Intentional Bugsnag error")
