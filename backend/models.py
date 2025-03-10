from app import db

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    club_name = db.Column(db.String(100), nullable=False)
    event_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String(200), nullable=True)

    def to_json(self):
        return {
            "id": self.id,
            "clubName": self.club_name,
            "eventName": self.event_name,
            "description": self.description,
            "location": self.location,
            "imgUrl": self.img_url,
        }

    