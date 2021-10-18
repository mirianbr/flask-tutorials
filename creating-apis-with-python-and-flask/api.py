"""Python API tutorial using Flask and SQLite3

Source: https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask

Supported endpoint examples (GET only):
    * Retrieve all the books or filtered by author, id and/or published
    * All books example:
    http://127.0.0.1:5000/api/v1/resources/books/all
    * Filtered by author example:
    http://127.0.0.1:5000/api/v1/resources/books?author=Connie+Willis
    * Filtered by published and author example:
    http://127.0.0.1:5000/api/v1/resources/books?author=Connie+Willis&published=1993

"""

import flask
import sqlite3

from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>This site is a prototype API for distant reading of science fiction novels.</p>'''


@app.errorhandler(404)
def page_not_found(e):
    return '''<h1>Ooops</h1>
<p>The page entered was not found. Please try a different URL.</p>''', 404


@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM books;').fetchall()

    return jsonify(all_books)


@app.route('/api/v1/resources/books', methods=['GET'])
def api_filter():
    query_params = request.args

    id = query_params.get('id')
    published = query_params.get('published')
    author = query_params.get('author')

    query = 'SELECT * FROM books WHERE'
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if published:
        query += ' published=? AND'
        to_filter.append(published)
    if author:
        query += ' author=? AND'
        to_filter.append(author)
    if not (id or published or author):
        return page_not_found(404)
    
    query = query[:-4] + ';'

    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    
    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)


app.run()