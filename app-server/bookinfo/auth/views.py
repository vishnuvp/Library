import ldap
from flask import request, render_template, flash, redirect, \
    url_for, Blueprint, g
from flask_login import current_user, login_user, \
    logout_user, login_required
from bookinfo import login_manager, db
from bookinfo.auth.models import User, LoginForm, EditBookForm
import requests 
import json
import os

BOOK_URL = os.getenv('BOOK_URL', "http://127.0.0.1:6000/book")
WORKER_URL = os.getenv('WORKER_URL', "http://127.0.0.1:6666/validate")
auth = Blueprint('auth', __name__)


 
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
 
 
@auth.before_request
def get_current_user():
    g.user = current_user
 
 
@auth.route('/')
@auth.route('/home')
def home():
    global BOOK_URL
    if current_user.is_authenticated:
        books = requests.get(BOOK_URL).json()
        current_user.set_books(books['_items'])
    return render_template('home.html')
 
 
@auth.route('/login', methods=['GET', 'POST'])
def login():
    global BOOK_URL

    if current_user.is_authenticated:
        flash('You are already logged in.')
        books = requests.get(BOOK_URL).json()
        current_user.set_books(books['_items'])
        print(current_user.books)
        return redirect(url_for('auth.home'))
 
    form = LoginForm(request.form)
 
    if request.method == 'POST' and form.validate():
        username = request.form.get('username')
        password = request.form.get('password')
        print("Got username", username, "password", password)
 
        try:
            User.try_login(username, password)
        except ldap.INVALID_CREDENTIALS:
            flash(
                'Invalid username or password. Please try again.',
                'danger')
            return render_template('login.html', form=form)
 
        user = User.query.filter_by(username=username).first()
        books = requests.get(BOOK_URL).json()
        if not user:
            user = User(username, password,books['_items'])
            db.session.add(user)
            db.session.commit()
        
        login_user(user)
        current_user.set_books(books['_items'])
        
        flash('You have successfully logged in.', 'success')
        return redirect(url_for('auth.home'))
 
    if form.errors:
        flash(form.errors, 'danger')
 
    return render_template('login.html', form=form)

def validate(text):

    global WORKER_URL
    payload = "{\n\"text\": \""+ text +"\"\n}"
    headers = {
    'Content-Type': "application/json"
    }

    response = requests.request("POST", WORKER_URL, data=payload, headers=headers).json()
    if response['status'] == 'ok':
        return response['text'], True
    return "", False

@auth.route('/book', methods=['GET','POST'])
def book():
    global BOOK_URL
    global WORKER_URL
    if request.method == 'GET':
        id = request.args.get('id')
        books = requests.get(BOOK_URL+"/"+id).json()
        print("Got books", books)
        form = EditBookForm(bid=id,title=books['title'], author=books['author'], genre=", ".join(books['genre']))
        return render_template('book.html', form=form)

    if request.method == 'POST':
        title,ok = validate(request.form.get('title'))
        if not ok:
            flash("Invalid title", danger)
            redirect(url_for('auth.home'))
        author,ok = validate(request.form.get('author'))
        if not ok:
            flash("Invalid author", danger)
            redirect(url_for('auth.home'))
        genre,ok = validate(request.form.get('genre'))
        if not ok:
            flash("Invalid genre", danger)
            redirect(url_for('auth.home'))
        genre = [g.strip() for g in genre.split(",")]
        bid = request.form.get('bid')

        genre_payload = ",".join(['"'+g+'"' for g in genre])
        print('Url', bid)
        url = BOOK_URL+"/"+bid
        book = requests.get(url).json()

        payload = "{\"title\": \""+ title +"\",\n    \"author\": \""+ author +"\",\n    \"genre\": ["+ genre_payload +"]\n}"
        headers = {
                    'Content-Type': "application/json",
                    'If-Match': book['_etag'],
                }

        response = requests.request("PATCH", url, data=payload, headers=headers).json()
        print(response)
        if response['_status'] == 'ERR':
            err_text = ""
            for k in response['_issues']:
                err_text += k + ":" + response['_issues'][k] + '\n'

            flash(err_text, 'danger')
        elif response['_status'] == 'OK':
            flash('Book updated', 'success')

    return redirect(url_for('auth.home'))    
        
        
        


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.home'))