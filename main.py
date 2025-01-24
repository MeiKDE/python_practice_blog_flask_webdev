from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, inspect, text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date
import os


"""
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
"""

app = Flask(__name__)
app.config["SECRET_KEY"] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
Bootstrap5(app)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


basedir = os.path.abspath(os.path.dirname(__file__))  # Get the directory of main.py
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(basedir, 'instance', 'posts.db')}"
)
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Print Database URI
print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


# Add a debug statement to ensure the database connection works:
with app.app_context():
    try:
        db.create_all()
        print("Database connected and table created successfully")

        # Inspect the Table Schema
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"Tables in the database: {tables}")
        columns = inspector.get_columns("blog_post")
        print(f"check columns: {columns}")

        # Check Table Records with Raw SQL
        raw_result = db.session.execute(text("SELECT * from blog_post")).fetchall()
        print(f"Raw SQL query result: {raw_result}")
    except Exception as e:
        print(f"Database connection error: {e}")


# WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


@app.route("/")
def get_all_posts():
    try:
        # Query all blog posts using ORM
        result = db.session.execute(db.select(BlogPost))
        posts = result.scalars().all()
        print(f"Number of records fetched: {len(posts)}")
        for post in posts:
            print(f"Post Title: {post.title}, Author: {post.author}")
    except Exception as e:
        print(f"Error fetching records: {e}")
        posts = []  # Return an empty list in case of errors
    return render_template("index.html", all_posts=posts)


# TODO: Add a route so that you can click on individual posts.
@app.route("/post/<int:post_id>")
def show_post(post_id):
    # TODO: Retrieve a BlogPost from the database based on the post_id
    requested_post = db.get_or_404(BlogPost, post_id)
    return render_template("post.html", post=requested_post)


# TODO: add_new_post() to create a new blog post
@app.route("/new-post", methods=["GET", "POST"])
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=form.author.data,
            date=date.today().strftime("%B %d, %Y"),
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


# TODO: edit_post() to change an existing blog post
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body,
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = edit_form.author.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)


# TODO: delete_post() to remove a blog post from the database
@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for("get_all_posts"))


# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)

"""with app.app_context():
    try:
        # Add sample blog posts
        sample_posts = [
            BlogPost(
                title="Sample Post 1",
                subtitle="This is a subtitle for Post 1",
                date=date.today().strftime("%B %d, %Y"),
                body="This is the body of the first sample post.",
                author="Author 1",
                img_url="https://example.com/image1.jpg",
            ),
            BlogPost(
                title="Sample Post 2",
                subtitle="This is a subtitle for Post 2",
                date=date.today().strftime("%B %d, %Y"),
                body="This is the body of the second sample post.",
                author="Author 2",
                img_url="https://example.com/image2.jpg",
            ),
        ]

        # Add and commit the sample posts
        db.session.add_all(sample_posts)
        db.session.commit()
        print("Sample posts added to the database.")
    except Exception as e:
        print(f"Error adding sample posts: {e}")
"""
