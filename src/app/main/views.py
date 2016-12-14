#coding=utf-8
'''
Created on 2016年12月14日

@author: huangning
'''
from flask import Flask,render_template,abort,redirect, request, url_for, flash,current_app,make_response
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from . import main

@main.route('/')
def index():
    return render_template('home.html')


@main.route('/blog')
def blog_index():
    return render_template('blog_index.html')


