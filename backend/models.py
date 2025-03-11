from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    club_name = db.Column(db.String(100), nullable=False)
    event_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String(200), nullable=True)

    def event_to_json(self):
        return {
            "id": self.id,
            "clubName": self.club_name,
            "eventName": self.event_name,
            "description": self.description,
            "location": self.location,
            "imgUrl": self.img_url,
        }
    
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String(200), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def profile_to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
            "imgUrl": self.img_url,
        }



    