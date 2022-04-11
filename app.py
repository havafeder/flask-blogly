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
@app.route('/tags')
def tags_index():
    """Show page with info on tags"""

    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def tags_show(tag_id):
    """Show info on a tag"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('show_tag.html', tag=tag)

@app.route('/tags/new')
def add_tag():
    """Show form to add new tag"""

    posts = Post.query.all()
    return render_template('new_tag.html', posts=posts)

@app.route("/tags/new", methods=["POST"])
def new_tags():
    """Handle form submission for creating new tag"""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>edit')
def edit_tag_form(tag_id):
    """Show form to edit tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tags/edit.html', tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tags(tag_id):
    """Handle for submission for editing tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """Handle form submission for deleting tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    
    return redirect('/tags')
