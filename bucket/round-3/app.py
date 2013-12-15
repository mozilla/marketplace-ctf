import json
import urllib

from flask import Flask, redirect, render_template, request, session

app = Flask(__name__)

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

    if 'token' not in parsed:
        session.update({'outcome': False,
                        'msg': 'No payment verification token'})
        return redirect('/')

    try:
        res = urllib.urlopen('https://ctf-checker-paas.allizom.org?%s'
                             % urllib.urlencode({'token': parsed['token']}))

        check = json.loads(res.content).get('valid')
    except:
        session.update({'outcome': False, 'msg': 'Failed token check'})
        return redirect('/')

    session.update({'outcome': True, 'msg': 'So verified, well done.'})
    return redirect('/')


@app.route('/clear')
def clear():
    del session['outcome']
    del session['msg']
    return redirect('/')


if __name__ == '__main__':
    app.secret_key = 'this-is-almost-the-round-in-the-middle'
    app.debug = True
    app.run()
