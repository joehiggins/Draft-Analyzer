# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 15:59:15 2017

@author: Joe
"""

#!flask/bin/python
from application import application
if __name__ == '__main__':
    application.debug = True
    port = int(os.environ.get("PORT", 5000))
    application.run(host='0.0.0.0', port=port)