# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 15:59:15 2017

@author: Joe
"""

from flask import render_template
from application import application

@application.route('/')
@application.route('/index')
def index():
    user = {'nickname': 'Hoe Jiggins'}  # fake user
    return render_template('index.html',
                           title='Draft Analyzer',
                           user=user)