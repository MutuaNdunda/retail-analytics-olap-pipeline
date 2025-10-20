#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask API to stream live POS transactions
@author: Gabriel
"""
from flask import Flask, Response, render_template, jsonify
from pos_stream import transaction_stream
import json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("dashboard.html")

@app.route("/stream")
def stream():
    def event_stream():
        for record in transaction_stream():
            yield f"data: {json.dumps(record)}\n\n"
    return Response(event_stream(), mimetype="text/event-stream")

@app.route("/latest")
def latest():
    """Single fetch endpoint for polling"""
    record = next(transaction_stream())
    return jsonify(record)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
