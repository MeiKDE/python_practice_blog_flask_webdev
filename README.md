# Flask Blog Application

This project is a simple blog application built using Flask. It demonstrates the use of Flask for web development, including database integration with SQLAlchemy, form handling with Flask-WTF, and rich text editing with Flask-CKEditor.

---

## Features

- Create, read, update, and delete blog posts.
- Use Bootstrap for responsive UI design.
- Store blog data in a SQLite database using SQLAlchemy ORM.
- Add rich text content to blog posts using Flask-CKEditor.
- Validate form inputs using Flask-WTF.

---

## Requirements

- Python 3.7+
- Flask
- Flask-Bootstrap
- Flask-SQLAlchemy
- Flask-WTF
- Flask-CKEditor
- WTForms
- SQLAlchemy


flask-blog/
├── instance/
│   └── posts.db           # SQLite database file
├── templates/
│   ├── index.html         # Home page template
│   ├── make-post.html     # Template for adding/editing posts
│   ├── post.html          # Template for viewing individual posts
│   ├── about.html         # About page template
│   └── contact.html       # Contact page template
├── static/
│   └── (optional static assets like CSS or images)
├── main.py                # Main application code
├── requirements.txt       # Dependencies
└── README.md              # Project documentation


