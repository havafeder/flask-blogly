"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

db.create_all()

@app.route('/')
def list_users():
	"""List users and show form."""

	users = User.query.all()

	return render_template("list.html", users=users)

@app.route("/", methods=["POST"])
def add_user():
    """Add user and redirect to list."""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] or None

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect("/")

@app.route("/<int:user_id>")
def show_pet(user_id):
    """Show info on a single user."""

    user = User.query.get_or_404(user_id)
    return render_template("detail.html", user=user)

@app.route('/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    """Handle form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/")


@app.route('/<int:user_id>/edit', methods=["GET"])
def users_update(user_id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)

@app.route('/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/")


@app.route('/users/<int:user_id>/add_post')
def post_form(user_id):
    """go to add_post form"""
    user = User.query.get_or_404(user_id)
    first_name = user.first_name

    return render_template('add_post.html', user=user, first_name=first_name)

@app.route('/users/<int:user_id>/add_post', methods=["POST"])
def add_post(user_id):
    """Form submission for creating new post"""

    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'], user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f"/{user_id}")

@app.route('/posts/<int:post_id>')
def show_posts(post_id):
    """Show info on specific post"""

    post = Post.query.get_or_404(post_id)
    return render_template("show_posts.html", post=post)

@app.route('/posts/<int:post_id>/edit', methods=["GET"])
def edit_post(post_id):
    """Show form to edit post"""

    post = Post.query.get_or_404(post_id)
    return render_template("edit_post.html", post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post(post_id):
    """Handle form submission for updating post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f"/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Handle form submission for deleting a post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    return redirect(f"/{post.user_id}")
