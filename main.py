from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:launchcode123@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RU'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(300))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password 


@app.before_request
def require_login():
    allowed_routes = ['login', 'blog_listing', 'index', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        else:
          flash('User password incorect or username does not exist', 'error')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    username_error = ''
    password_error = ''
    verify_error = ''
    user_duplicate_error = ''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verifypassword = request.form['verifypassword']

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        elif existing_user:
            user_duplicate_error = "Username already exists."
        elif username == "":
            username_error = "Please submit a valid username."
        elif len(username) < 3:
            username_error = "Please submit a username longer than 3 characters."
        elif password == "":
            password_error = "Please submit a valid password."
        elif len(password) < 3:
            password_error = "Please submit a password longer than 3 characters."
        elif verifypassword == "":
            verify_error = "Please verify your password."
        elif password != verifypassword:
            password_error = "Your passwords do not match."
            verify_error = "Your passwords do not match"
            username = request.form['username']
            password = ""
            verifypassword = ""
    else:
        return render_template('signup.html', username_error=username_error, password_error=password_error, verify_error=verify_error)

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

@app.route('/blog', methods=['GET', 'POST'])
def blog_listing():
    blog_id = request.args.get('id')
    user_id = request.args.get('user') # 'user' variable from query parameter right after ? is equal to 'user' in get request

    if blog_id == None and user_id == None:
        blogs = Blog.query.all()
        return render_template('blog.html', completed_blogs=blogs)

    if blog_id:
        blog = Blog.query.filter_by(id=blog_id).first()
        return render_template('template.html', blog=blog)
    
    if user_id != None:
        blog = Blog.query.filter_by(owner_id=user_id).all() # blue variable is from Class Blog = to variable from get request
        return render_template('userposts.html', completed_blogs=blog)




@app.route('/newpost', methods=['GET','POST'])
def new_post():
    
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        owner = User.query.filter_by(username=session['username']).first()
        
        if title == "":
            flash('Please submit a blog title.', 'error')
            return render_template('newpost.html', title=title, body=body)
        if body == "":
            flash('Please fill in a blog post.', 'error')
            return render_template('newpost.html', title=title, body=body)
        
        new_blog = Blog(title, body, owner)
        db.session.add(new_blog)
        db.session.commit()
        return redirect('/blog?id=' + str(new_blog.id))
    else: 
        return render_template('newpost.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

    
if __name__ == '__main__':
    app.run()
