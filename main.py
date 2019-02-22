from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:local@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(999))

    def __init__(self, name):
        self.name = name
        # self.completed = False

@app.route('/blog')
def index():
    
    posts = Blog.query.all()
    # completed_tasks = Blog.query.filter_by(completed=True).all()
    return render_template('blog.html', posts=posts)


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':
        post_name = request.form['post']
        new_post = Blog(post_name)
        db.session.add(new_post)
        db.session.commit()

    return render_template('blog.html')

"""
@app.route('/delete-task', methods=['POST'])
def delete_task():

    task_id = int(request.form['task-id'])
    task = Blog.query.get(task_id)
    task.completed = True
    db.session.add(task)
    db.session.commit()

    return redirect('/')
"""

if __name__ == '__main__':
    app.run()