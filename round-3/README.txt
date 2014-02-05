We've written this cool way to review web apps. Add an app as some JSON and
reviewers will access the review page. *Note* reviewers will visit any URL
given in the JSON.

Goal: **Access the review page**

To run: python app.py

To see what a reviewer would do run: phantomjs reviewer.js http://localhost:5000

That will show you how a reviewer would log in and what they would click on.
