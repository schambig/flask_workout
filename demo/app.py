from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps


app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first (inside wrap method)')
            return redirect(url_for('login'))
    return wrap


@app.route('/')
@login_required
def home():
    return render_template('index.html')


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again (inside login method)'
        else:
            session['logged_in'] = True
            flash('Welcome! (inside login method)')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('Good bye! (inside logout method)')
    return redirect(url_for('welcome'))


if __name__ == '__main__':
    app.run(debug=True)
