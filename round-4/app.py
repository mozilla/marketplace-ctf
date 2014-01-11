import json
import os
import uuid

from flask import Flask, redirect, render_template, request, session
from werkzeug.contrib.cache import MemcachedCache


app = Flask(__name__)
cache = MemcachedCache(['127.0.0.1:11211'])

if not os.path.exists('secret.json'):
    open('secret.json', 'w').write(str(uuid.uuid4()))


def logged_in(f):
    def wrapper():
        if not session.get('user'):
            session.update({'msg': 'Not allowed', 'user': False})
            return redirect('/')
        return f()
    return wrapper


@app.route('/', methods=['GET'])
def index():
    return render_template('page.html', session=session)


@app.route('/', methods=['POST'])
def parse():
    try:
        parsed = json.loads(request.form.get('manifest', ''))
    except ValueError:
        session.update({'outcome': False, 'msg': 'Could not parse JSON'})
        return redirect('/')

    res = cache.get('round-3:to-review')
    if not res:
        res = []
    res.append({'data': parsed, 'key': str(uuid.uuid4()),
                'status': 'unreviewed'})
    cache.set('round-4:to-review', res)
    session.update({'msg': 'Added to the review queue.'})
    return redirect('/')



@logged_in
@app.route('/review', methods=['GET'])
def review():
    return render_template('review.html', session=session,
                           reviews=cache.get('round-4:to-review') or [],
                           request=request)


@logged_in
@app.route('/status', methods=['POST'])
def status():
    key = request.form.get('key')
    reviews = cache.get('round-4:to-review') or []
    for review in reviews:
        if review['key'] == key:
            review['status'] = request.form.get('status')
    cache.set('round-4:to-review', reviews)
    return redirect('/review')



@app.route('/login')
def login():
    if request.args.get('key') == open('secret.json', 'r').read():
        session.update({'msg': '', 'user': True})
        return redirect('/review')

    session.update({'msg': 'Not allowed', 'user': False})
    return redirect('/')


@app.route('/clear')
def clear():
    session.pop('msg', None)
    session.pop('user', None)
    return redirect('/')


if __name__ == '__main__':
    app.secret_key = 'this-is-almost-the-round-in-the-middle'
    app.debug = True
    app.run()
