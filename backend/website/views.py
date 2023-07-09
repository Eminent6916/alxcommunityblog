from flask import Blueprint, render_template,  redirect, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import random
import datetime
from .models import Post, User, Comment, Like
from . import db


 
views = Blueprint('views', __name__)

@views.route('/home')
@views.route('/index')
@views.route("/")
def index():
    return render_template("index.html", user=current_user)


@views.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    user = User.query.filter_by(username=current_user.username).first()
    posts = Post.query.filter_by(user_id=user.id).all()
    if request.method == "POST":
        title = request.form.get('title')
        body = request.form.get('body')
        tags = request.form.get('tags')
        code = request.form.get('code')
        twords = title.split(" ")
        tslug = ""
        for word in twords:
            if tslug == '-'+twords[0]:
                 tslug=twords[0]
            tslug = tslug + '-' + word

        hslug = str(random.randint(0, 20)) + current_user.username
        title_exists = Post.query.filter_by(title=title).first()
        if not title:
            flash('Title is required', category='error' )
        elif title_exists:
            flash('Ttile already in use. Reframe.', category='error')
        elif not body: 
            flash('Body is required', category='error' )
        else:
            post = Post(title = title,
                        body = body,
                        tags = tags,
                        code = code,
                        tslug = tslug,
                        slug = generate_password_hash(hslug, method='sha256'),
                        user_id = current_user.id)
            
            db.session.add(post)
            db.session.commit()
            flash('Post created successfully', 'success')
            return redirect(url_for('views.post'))

    return render_template("addpost.html", user=current_user, posts=posts )

@views.route('/blog')
@views.route('/posts')
def post():
    posts = Post.query.all()
    return render_template('posts.html', user=current_user, posts=posts)


@views.route("/delete-post/<slug>")
@login_required
def delete_post(slug):
    post = Post.query.filter_by(slug=slug).first()
    ad = User.query.filter_by(username='admin6916').first()
  
    if not post:
        flash("No post found", category='error')
    elif ad.username =='admin6916':
        db.session.delete(post)
        db.session.commit()
        flash("Post Deleted Successfully", category='success')
    elif current_user.id != post.user_id: 
        flash("You are not allowed to delete this post", category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post Deleted Successfully", category='success')
    return redirect(url_for('views.post'))
@views.route("/post/<query>") 
def posts(query):
        user = User.query.filter_by(username=query).first()
        post_tslug = Post.query.filter_by(tslug=query).all()
        post_user= Post.query.filter_by(user_id=current_user.id).all()
        posts = Post.query.all()

   
        if post_user:
            posts = post_user
            return render_template("posts.html", user=current_user, posts=post_user, header= query.title() +"'s Posts" )
        elif post_tslug:
            return render_template("singlepost.html", user=current_user, posts=post_tslug, header= "Post")
        elif not post_user or not post_tslug:
            flash('No Post Found', 'error')
            return render_template("posts.html", user=current_user, posts=posts)\
            
@views.route("/post/details/<query>") 
def details(query):
        post_user = User.query.filter_by(username=query).first()
        # post_user= Post.query.filter_by(user_id=user.id).all()
        post_tslug = Post.query.filter_by(tslug=query).all()
        posts = Post.query.all()
   
        if post_user:
            posts = post_user
            return render_template("posts.html", user=current_user, posts=post_user, header= query.title() +"'s Posts" )
        elif post_tslug:
            return render_template("singlepost.html", user=current_user, posts=post_tslug, header= "Post")
        elif not post_user or not post_tslug:
            flash('No Post Found', 'error')
            return render_template("posts.html", user=current_user, posts=posts)

@views.route('/create-comment/<query>', methods=["POST"])
@login_required
def create_comment(query):
    body = request.form.get('body')
    code = request.form.get('code')

    if not body:
        flash("Comment cannot be blank", category="error")
    else:
        post = Post.query.filter_by(tslug = query).first()
        if post:
            username = current_user.username
            slug = generate_password_hash(username + str(datetime.datetime.now()))
            comment = Comment(body= body, 
                              code= code, 
                              user_id=current_user.id, 
                              slug =slug, 
                              post_id= post.id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash("Post does not exist", category="error")

    return redirect(url_for('views.details', query=post.tslug))

@views.route("/delete-comment/<slug>")
@login_required
def delete_comment(slug):
    ad = User.query.filter_by(username='admin6916').first()
    comment = Comment.query.filter_by(slug=slug).first()
    post = Post.query.filter_by(id=comment.post_id).first()
    if not comment:
        flash("Noting Found", category='error')
    elif ad.username =='admin6916':
        db.session.delete(comment)
        db.session.commit()
        flash("Post Deleted Successfully", category='success')
    elif current_user.id != comment.user_id and current_user.id != comment.post.user_id:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    posts = Post.query.all()
    return redirect(url_for('views.details', query=post.tslug))

@views.route("/like-post/<query>",  methods=["GET"])
@login_required
def like(query):
    post = Post.query.filter_by(tslug=query).first()
    
    like = Like.query.filter_by(user_id=current_user.id, post_id = post.id).first()

    if not post:
        flash('Post not found', category='error')
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(user_id=current_user.id, post_id=post.id)
        db.session.add(like)
        db.session.commit()
    return redirect(url_for('views.details', query=query))

@views.route('/profile')
@views.route('/profile/')
@views.route("/profile/<username>", methods=['GET', 'POST'])
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    posts = Post.query.filter_by(user_id=user.id).all()
    return render_template('profile.html', user=current_user, posts = posts)

@views.route('/about')
def about():
    return render_template('about.html', user=current_user)