#coding=utf-8
'''
Created on 2016年12月14日

@author: huangning
'''
from flask import Blueprint

main = Blueprint('main', __name__)

from . import views

#add comment