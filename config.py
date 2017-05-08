# -*- coding:utf-8 -*-
"""
Author: Tianxiao Hu
Last Modified: 2017.5.5
Email: hutianxiao_fdu@126.com
Project for Introduction to Database Systems(COMP130010.03)@Fudan University
"""
import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_LOC = os.path.join(basedir, 'app.db')

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

# pagination
PAGINATION_PER_PAGE = 5
