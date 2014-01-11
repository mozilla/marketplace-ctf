import json
import os
import uuid

from flask import Flask, redirect, render_template, request, session
from werkzeug.contrib.cache import MemcachedCache


app = Flask(__name__)
cache = MemcachedCache(['127.0.0.1:11211'])

if not os.path.exists('secret.json'):
    open('secret.json', 'w').write(str(uuid.uuid4()))


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
    res.append(parsed)
    cache.set('round-3:to-review', res)
    session.update({'msg': 'Added to the review queue.'})
    return redirect('/')


@app.route('/review', methods=['GET'])
def review():
    if not request.args.get('key') == open('secret.json', 'r').read():
        return redirect('/')
    return render_template('review.html', session=session,
                           reviews=cache.get('round-3:to-review') or [],
                           request=request)


@app.route('/clear')
def clear():
    del session['msg']
    return redirect('/')


if __name__ == '__main__':
    app.secret_key = 'this-is-almost-the-round-in-the-middle'
    app.debug = True
    app.run()
