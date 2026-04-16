
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# This tells Flask where to save your database file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
db = SQLAlchemy(app)

# This is a 'Model' - it's like a template for your Database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

@app.route('/')
def home():
    return "<h1>Online Quiz Platform is running!</h1>"

if __name__ == '__main__':
    app.run(debug=True)
    