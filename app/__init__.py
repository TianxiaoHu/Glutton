# -*- coding:utf-8 -*-
"""
Author: Tianxiao Hu
Last Modified: 2017.5.5
Email: hutianxiao_fdu@126.com
Project for Introduction to Database Systems(COMP130010.03)@Fudan University
"""
from flask import Flask
app = Flask(__name__)
app.config.from_object('config')
from app import views
