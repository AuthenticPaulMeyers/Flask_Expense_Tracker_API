from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(90), nullable=False, unique=True)
    email = db.Column(db.String(90), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    expense=db.Relationship('Expense', backref='user')
    def __repr__(self) -> str:
        return f'User>>> {self.username}'

class Expense(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey("user.id"))
    category_id=db.Column(db.Integer, db.ForeignKey("category.id"))
    amount=db.Column(db.Integer, nullable=False)
    description=db.Column(db.Text, unique=False, nullable=False)
    date=db.Column(db.DateTime, default=datetime.now())
    def __repr__(self) -> int:
        return f'Expense>>> {self.id}'

class Category(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90), nullable=False, unique=True)
    expense=db.Relationship('Expense', backref='category')
    def __repr__(self) -> int:
        return f'Category>>> {self.id}'
