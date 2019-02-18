# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 13:16:48 2019

@author: Davis
"""

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!