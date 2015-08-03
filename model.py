"""Model for RoomEase site."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()

###################################################################
# Model Definitions

class User(db.Model):
    """User of RoomEase website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True, unique=True)
    password = db.Column(db.String(64), nullable=True)
    name = db.Column(db.String(30), nullable=False)
    house_id = db.Column(db.Integer, ForeignKey('houses.house_id'), nullable=False)
    phone = db.Column(db.Integer, nullable=False, unique=True)


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s house_id= %s email=%s>" % (self.user_id, self.house_id, self.email)

class House(db.Model):
    """Model for each individual group of roommates (houses)."""

    __tablename__ = "houses"

    house_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    address = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<House house_id=%s address=%s>" % (self.house_id, self.address)

	# Define relationship to user
    user = db.relationship("User", backref=db.backref("houses", order_by=house_id))

	# Define relationship to bill
    bill = db.relationship("Bill", backref=db.backref("houses", order_by=house_id))

class Bill(db.Model):
    """Model for each individual bill for a house."""

    __tablename__ = "bills"

    bill_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    house_id = db.Column(db.Integer, ForeignKey('houses.house_id'), nullable=False)
    due_date = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Bill bill_id=%s house_id=%s description=%s due_date=%s amount=%s>" % (self.bill_id, self.house_id, self.description, self.due_date, self.amount)

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///roomease.db'
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."