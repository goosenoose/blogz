from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:local@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    date = db.Column(db.DateTime)

    def __init__(self, title, body, date=None):
        self.title = title
        self.body = body
        if date is None:
            date = datetime.utcnow()
        self.date = date

@app.route('/')
def index():
    return redirect('/blog')

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    post_id = request.args.get('id')
    title = "Build-a-Blog"

    if post_id:
        blog = Blog.query.filter_by(id=post_id).all()
        date = Blog.query.filter_by(date=post_id).all()
        return render_template('blog.html', title=title, blog=blog, post_id=post_id, date=date)
    else:
        blog = Blog.query.order_by(Blog.id.desc()).all()
        date = Blog.query.filter_by(date=post_id).all()
        return render_template('blog.html', title=title, blog=blog, date=date)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        post_title = request.form['posttitle']
        post_body = request.form['postbody']
        title_error = ''
        body_error = ''

        if not post_title:
            title_error = "Please enter a title for post"
        if not post_body:
            body_error = "Please enter content for post"

        if not body_error and not title_error:
            new_post = Blog(post_title, post_body)
            db.session.add(new_post)
            db.session.commit()
            return redirect('/blog?id={}'.format(new_post.id))
        else:
            return render_template('newpost.html', title='New Post', title_error=title_error, body_error=body_error, posttitle=post_title, postbody=post_body)
    
    return render_template('newpost.html', title='New Post')

if  __name__ == "__main__":
    app.run()