import sqlite3
import uuid

from flask import Flask, redirect, render_template, request, session

DATABASE = 'the.db'


def get_db():
    return sqlite3.connect(DATABASE)

app = Flask(__name__)

cmds = [
    """CREATE TABLE IF NOT EXISTS users
    (user varchar(255), password varchar(255), UNIQUE (user));""",
    # You could login using the password below, but thats not the point.
    "INSERT OR IGNORE INTO users (user, password) VALUES ('admin', '%s');" %
    uuid.uuid4()
]

db = get_db()
for cmd in cmds:
    db.cursor().execute(cmd)
    db.commit()


@app.route('/', methods=['GET'])
def index():
    return render_template('page.html', user=session.get('user'))


@app.route('/', methods=['POST'])
def login():
    db = get_db()
    sql = "SELECT user FROM users WHERE user = '%s' AND password = '%s'" % (
        request.form['user'], request.form['password'])
    res = db.cursor().execute(sql).fetchone()
    if res:
        session['user'] = res[0]

    return redirect('/')


@app.route('/logout')
def logout():
    del session['user']
    return redirect('/')


if __name__ == '__main__':
    app.secret_key = 'round-1-baby'
    app.debug = True
    app.run()
