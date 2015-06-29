#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File Name : sql.py
'''Purpose : Intro sth                                 '''
# Creation Date : 1435545244
# Last Modified :
# Release By : Doom.zhou
###############################################################################


from flask import Flask, g
import sqlite3


app = Flask(__name__)
def connect_db():
    """Returns a new connection to the sqlite database"""
    return sqlite3.connect('doom.db', detect_types=sqlite3.PARSE_DECLTYPES)


def query_db(query, args=(), one=False):
    """Query database returning dictionary"""
    cur = g.db.execute(query, args)
    rv = [dict(
        (cur.description[idx][0], value)
        for idx, value in enumerate(row)) for row in cur.fetchall()
        ]
    return (rv[0] if rv else None) if one else rv


@app.before_request
def before_request():
    g.db = connect_db()


@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/')
def index():
    sumstr = ''
    results = g.db.execute('select username, login_time, logout_time \
from vpns order by login_time desc limit 12').fetchall()
    for i, result in enumerate(results):
        print(result)
    return sumstr


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
