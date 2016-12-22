#coding=utf-8
'''
Created on 2016年12月14日

@author: huangning
'''
from flask import Flask,render_template,abort,redirect, request, url_for, flash,current_app,make_response,send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from ..models import User,Post,Comment
from .forms import RegistrationForm,LoginForm,PostForm,CommentForm,CategoryForm
from . import main
from .. import db
from app.models import Category_or_Tag
from datetime import datetime, timedelta
 

@main.route('/',methods=['GET','POST'])
def index():
  
    return render_template('home.html')


@main.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are member now,please log in ')
        return redirect(url_for('main.login'))
    return render_template('register.html',form=form)


@main.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('main.blog_index'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@main.route('/blog/list',methods=["GET",'POST'])
@login_required
def blog_index():
    show_recent = False
    if current_user.is_authenticated:
        show_recent = bool(request.cookies.get('show_recent', ''))
    if show_recent:
        print datetime.now()
        print Post.query.first().timestamp
        blogs = Post.query.filter(Post.timestamp > str(datetime.now()-timedelta(days=3))).order_by(Post.timestamp.desc())
    else:
        blogs = Post.query.order_by(Post.timestamp.desc())
    return render_template('blog_index.html',blogs=blogs)
    #return login()


@main.route('/blog/edit',methods=["GET",'POST'])
@login_required
def edit_blog():

    '''if current_user != post.author and \
    not current_user.can(Permission.ADMINISTER):
        abort(403)'''
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data,category_id=form.category.data,author=current_user._get_current_object())
        
        db.session.add(post)
        #db.commit()
        flash('The post has been updated.')
        return redirect(url_for('main.blog_index'))
    #form.body.data = post.body
    return render_template('edit_post.html', form=form)
    
    
@main.route('/blog/<int:id>',methods=["GET",'POST'])
@login_required
def blog(id):
    post = Post.query.get_or_404(id)
    
    return render_template('post.html', posts=[post])

@main.route('/category/add',methods=['GET','POST'])
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category_or_Tag(name=form.name.data,
                    istag = False)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('main.category'))
    return render_template('add_category.html',form=form)

@main.route('/category',methods=['GET','POST'])
def category():
    categorys = Category_or_Tag.query.filter_by(istag=False).order_by(Category_or_Tag.name)
    return render_template('category.html',categorys=categorys)


@main.route('/blog/recent')
def show_recent():
    resp = make_response(redirect(url_for('main.blog_index')))
    resp.set_cookie('show_recent', '1',max_age=5*60)
    return resp

@main.route('/blog/all')
def show_all():
    resp = make_response(redirect(url_for('main.blog_index')))
    resp.set_cookie('show_recent', '',max_age=5*60)
    return resp


@main.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'],filename)




