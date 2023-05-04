from main import db,login_manager
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    password = db.Column(db.String(60),nullable=False)
    isAdmin = db.Column(db.Boolean,default=False)

    def __repr__(self):
        return f'User {self.username}, {self.email}'
    
class Venue(db.Model):
    venue_id = db.Column(db.Integer,primary_key=True)
    venue_name = db.Column(db.String(20),nullable=False)
    venue_address = db.Column(db.String(120),unique=True,nullable=False)
    venue_capacity = db.Column(db.Integer)
    venue_shows = db.relationship('Show', backref='venue', lazy=True)

    def __repr__(self):
        return f'Venue {self.venue_name}, {self.venue_capacity}'
    
class Show(db.Model):
    show_id = db.Column(db.Integer,primary_key=True)
    venue_id = db.Column(db.Integer,db.ForeignKey('venue.venue_id'), nullable=False)
    show_name = db.Column(db.String(20),unique=True,nullable=False)
    show_rating = db.Column(db.Integer)
    show_ticket_price = db.Column(db.Integer)
    
    def __repr__(self):
        return f'Show {self.show_name}, {self.show_ticket_price}, {self.show_rating}'

    
class Booking(db.Model):
    booking_id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    show_id = db.Column(db.Integer,db.ForeignKey('show.show_id'), nullable=False)
    quantity = db.Column(db.Integer,nullable=False)
    
    def __repr__(self):
        return f'Booking {self.booking_id}'