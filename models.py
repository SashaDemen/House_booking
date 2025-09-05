from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100))
    city = db.Column(db.String(100))
    type = db.Column(db.String(100))
    price = db.Column(db.Integer)
    size = db.Column(db.Integer)
    rooms = db.Column(db.Integer)
    description = db.Column(db.String(500))
    image_url = db.Column(db.String(200))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    owner = db.relationship('Users', backref='houses')

    def __repr__(self):
        return f"<House {self.id}, City: {self.city}>"

# models.py
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    reservation = db.Column(db.String(100))
    reservation_time = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Исправлено на 'users.id'
    house_id = db.Column(db.Integer, db.ForeignKey('house.id'))  # Исправлено на 'house.id'

    def __repr__(self):
        return f"<Booking {self.id}, House ID: {self.house_id}>"


