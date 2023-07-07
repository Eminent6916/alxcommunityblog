from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

 
app= Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///post.db'
db= SQLAlchemy(app)

class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(130), nullable=False)
    body = db.Column(db.text, nullable=False)
    tag = db.Column(db.string, nullable=True)
    image=db.column(db.string, nullable=True)
    author=db.column(db.string, nullable=False)
    created_at=db.column(db.datetime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return 'Blog post' + self.title

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/bj')
def singlepost():
    return render_template('singlepost.html')


@app.route('/addpost')
def addpost():
    return render_template('addpost.html')



if __name__ == "__main__":
    app.run(debug=True) 
