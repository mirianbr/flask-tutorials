"""A Minimal Application

From https://flask.palletsprojects.com/en/2.0.x/quickstart/
"""


from flask import Flask, render_template, request, url_for
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def index():
    return "Index Page"


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/login')
def login():
    return 'login'


@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'


with app.test_request_context():
    print(url_for('index'))
    print(url_for('hello'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))