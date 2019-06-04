# -*- coding: utf-8 -*-
# @Time    : 2019-05-20 12:21
# @Author  : Woko
# @File    : app.py

import os
from functools import wraps

import requests
from authlib.flask.client import OAuth
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from six.moves.urllib.parse import urlencode
from werkzeug.exceptions import HTTPException

app = Flask(__name__, template_folder='./template')
app.debug = True
app.secret_key = 'secret'

oauth = OAuth(app)

os.environ.setdefault('AUTHLIB_INSECURE_TRANSPORT', '1')  # use http

CLIENT_ID = 'YOUR-CLIENT-ID'
CLIENT_SECRET = 'YOUR-CLIENT-SECRET'

REDIRECT_URI = 'http://127.0.0.1:3000/callback'

auth0 = oauth.register(
    'woko_test',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    api_base_url='http://127.0.0.1:5000',
    access_token_url='http://127.0.0.1:5000/oauth/token',
    authorize_url='http://127.0.0.1:5000/oauth/authorize',
    client_kwargs={
        'scope': 'profile',
    },
)


# Here we're using the /callback route.
@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    token = auth0.authorize_access_token()

    # If it's a jwt, we can decode from it,
    # otherwise get from userinfo api like this
    res = oauth.woko_test.get('/api/me')  # type: requests.Response
    userinfo = res.json()

    # Store the user information in flask session.
    session['profile'] = {
        'user_id': userinfo['id'],
        'name': userinfo['username'],
    }
    return redirect('/dashboard')


@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=REDIRECT_URI)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            # Redirect to Login page here
            return redirect('/')
        return f(*args, **kwargs)

    return decorated


@app.route('/dashboard')
@requires_auth
def dashboard():
    return render_template('dashboard.html', userinfo=session['profile'])


@app.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('home', _external=True),
              'client_id': CLIENT_ID}
    return redirect(auth0.api_base_url + '/logout?' + urlencode(params))


@app.errorhandler(Exception)
def handle_auth_error(ex):
    response = jsonify(message=str(ex))
    response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
    return response


# Controllers API
@app.route('/')
def home():
    return render_template('home.html')


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=3000)
