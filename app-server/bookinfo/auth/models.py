import ldap
from flask_wtf import Form
from wtforms import TextField, PasswordField, HiddenField
from wtforms.validators import InputRequired
from bookinfo import db, app
 
 
def get_ldap_connection():
    print("initializing ldap connection")
    conn = ldap.initialize(app.config['LDAP_PROVIDER_URL'])
    print("Connection object:", conn)
    return conn

 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    books = []
 
    def __init__(self, username, password, books):
        self.username = username
        self.books = books
    def set_books(self, books):
        self.books = []
        for i in books:
            u = i['_links']['self']['href'].split('/')
            self.books.append([i['title'],i['author'],i['genre'],u[0]+"?id="+u[1]])
        
    def get_books(self):
        return self.books 
    @staticmethod
    def try_login(username, password):
        conn = get_ldap_connection()
        conn.simple_bind_s(
            'cn=%s,ou=users,dc=glauth,dc=com' % username,
            password
        )
 
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        print("Returning id", self.id)
        return self.id

class EditBookForm(Form):
    title = TextField('Title', [InputRequired()])
    author = TextField('Author',[InputRequired()])
    genre = TextField('Genre',[InputRequired()])
    bid = HiddenField('Bid')
 
class LoginForm(Form):
    username = TextField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])