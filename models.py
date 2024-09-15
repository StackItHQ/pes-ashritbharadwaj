# models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Customer(db.Model):
    __tablename__ = 'students'

    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Section = db.Column(db.String(5), nullable=False)
    College = db.Column(db.String(50), nullable=False)
    RollNumber = db.Column(db.String(10), nullable=False, unique=True)

    def __repr__(self):
        return f"<Student {self.name}>"
