import sqlite3
import subprocess

from flask import Flask, redirect, render_template, request, session

DATABASE = 'the.db'


def get_db():
    return sqlite3.connect(DATABASE)

app = Flask(__name__)

cmds = [
    """CREATE TABLE IF NOT EXISTS users
    (user varchar(255), password varchar(255), UNIQUE (user));""",
    "INSERT OR IGNORE INTO users (user, password) VALUES ('admin', 'awooga');"
]

db = get_db()
for cmd in cmds:
    db.cursor().execute(cmd)
    db.commit()


@app.route('/', methods=['GET'])
def index():
    return render_template('page.html', session=session)


@app.route('/', methods=['POST'])
def login():
    db = get_db()
    sql = "SELECT user FROM users WHERE user = ? AND password = ?"
    user, password = request.form['user'], request.form['password']
    res = (db.cursor().execute(sql, (user, password)).fetchone())
    if res:
        session['user'] = res[0]
    else:
        try:
            cmd = 'cat hints/%s.txt' % user
            session['hints'] = subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError:
            # Hint doesn't exist for the user, skip.
            session['hints'] = ''

    return redirect('/')


@app.route('/logout')
def logout():
    del session['user']
    return redirect('/')


if __name__ == '__main__':
    app.secret_key = 'you-thought-round-1-was-bad?'
    app.debug = True
    app.run()
