#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import socket
import sqlite3
from flask import Flask, request, render_template, \
    jsonify, redirect, g
# from dateutil.parser import parse
# from datetime import datetime

# Support for gomix's 'front-end' and 'back-end' UI.
app = Flask(__name__, static_folder='public', template_folder='views')
app.config.from_object('_config')

# Set the app secret key from the secret environment variables.
app.secret = os.environ.get('SECRET')

def connect_db():
    return sqlite3.connect(app.config['DATABASE_PATH'])

url_dict = {}
url_list = []

@app.route('/')
def homepage():
    """Displays thot hormeparger."""
    return render_template('index.html')
    
@app.route('/api/shorturl/<int:arg>', methods=['GET'])
def shorturl(arg):
    """Simple API my hoes anddreas.
    """
    g.db = connect_db()
    cur = g.db.execute(
        'select url from urls where url_id=' + str(arg) 
    )
    url_list = cur.fetchall()
    print(arg)
    if len(url_list) > 0:
        return redirect(url_list[0][0])
    return jsonify({"error" : "No short url found for given input"})
  
@app.route('/api/shorturl/new', methods=['POST'])
def newurl():
    url = request.form["url"]
    print(url)
    if url.startswith("https://"): url = url[8:]
    elif url.startswith("http://"): url = url[7:]
    try:
        socket.gethostbyname(url)
    except:
        return jsonify({"error":"invalid Hostname"})
    url = "http://" + url
    g.db = connect_db()
    cur = g.db.execute(
        'select url, url_id from urls where url="' + url + '"'
    )
    url_list = cur.fetchall()
    if len(url_list) > 0:
        return jsonify({
            "original_url":url_list[0][0],
            "short_url":url_list[0][1]
        })
    g.db.execute('insert into urls (url) values (?)', [url])
    cur = g.db.execute(
        'select url, url_id from urls where url="' + url + '"'
    )
    url_list = cur.fetchall()
    if len(url_list) > 0:
        g.db.commit()
        g.db.close()
        return jsonify({
            "original_url":url_list[0][0],
            "short_url":url_list[0][1]
        })
    return jsonify({
        "error":"SQL failure"
    })

if __name__ == '__main__':
    app.run()