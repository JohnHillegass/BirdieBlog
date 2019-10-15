from flask import Blueprint, render_template, redirect, url_for, request, flash
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from models import *
from flask_login import login_required, current_user, login_user
import json

engine = create_engine('sqlite:///blog.db')
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
session = Session()

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/posts/view/<int:post_id>', methods=['GET'])
def viewPost(post_id):
    post = session.query(Post).get(post_id)
    return render_template('post.html', post=post)


@main.route('/posts/create', methods=['GET','POST'])
def createPost():
    if request.method == 'POST':
        print(request)
        newPost = Post(
            request.form['title'], request.form['description'], request.form['content'], str(current_user.id)
        )
        session.add(newPost)
        session.commit()
        flash('CREATE')
        flash('Post created successfully')
        return redirect(url_for('main.myPosts'))
    else:
        return render_template('post-create.html')

@main.route('/posts/edit/<int:post_id>', methods=['GET'])
def editPost(post_id):
    post = session.query(Post).filter_by(id=post_id).one()
    return render_template('post-edit.html', post=post)

@main.route('/posts/update', methods=['POST'])
def updatePost():
    post = session.query(Post).filter_by(id=request.form['id']).one()
    post.name = request.form['title']
    post.description = request.form['description']
    post.content = request.form['content']
    session.add(post)
    session.commit()
    flash('SAVE')
    flash('saved post# ' + str(request.form['id']))
    return redirect(url_for('main.myPosts'))

@main.route('/posts/delete/<int:post_id>', methods=['GET'])
def deletePost(post_id):
    post = session.query(Post).filter_by(id=post_id).one()
    if post.author_id == current_user.id:
        session.delete(post)
        session.commit()
        flash('DELETE')
        flash('deleted post# ' + str(post_id))
    else:
        flash('DELETE')
        flash('you cannot delete someone else\'s post')
    return redirect(url_for('main.myPosts'))

@main.route('/posts/recent', methods=['GET'])
def recentPosts():
    posts = session.query(Post).all()
    return render_template('posts.html', posts=posts)


@main.route('/posts/my', methods=['GET'])
def myPosts():
    # check the author then render
    users = session.query(User).filter_by(id=current_user.id).first()
    print(users.posts)
    return render_template('posts.html', posts=users.posts, yourPosts=True)


@main.route('/profile', methods=['GET'])
def profile():
    return render_template('profile.html', user=current_user)
