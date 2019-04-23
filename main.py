from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode123@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RU'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(300))

    def __init__(self, title, body):
        self.title = title
        self.body = body

#user submits a blog and is redirected to main blog page
#displays blog posts on a main page called /blog
#add new blog posts on a form page called /newpost
#link blog title to individual blog page by id 

@app.route('/blog', methods=['GET', 'POST'])
def blog_listing():
    blog_id = request.args.get('id')

    if blog_id == None:
        blogs = Blog.query.all()
        return render_template('blog.html', completed_blogs=blogs)
    else:
        blog = Blog.query.filter_by(id=blog_id).first()
        return render_template('template.html', blog=blog)


@app.route('/newpost', methods=['GET','POST'])
def new_post():
    
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        if title == "":
            flash('Please submit a blog title.', 'error')
            return redirect('/newpost')
        if body == "":
            flash('Please fill in a blog post.', 'error')
            return redirect('/newpost')
        
        new_blog = Blog(title, body)
        db.session.add(new_blog)
        db.session.commit()
        return redirect('/blog?id=' + str(new_blog.id))
    else: 
        return render_template('newpost.html')


if __name__ == '__main__':
    app.run()
