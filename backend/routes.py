from app import app, db
from flask import request, jsonify
from models import Event, Profile

@app.route("/events", methods=["GET"])
def get_events():
    events = Event.query.all()
    result = [event.event_to_json() for event in events]
    return jsonify(result), 200

@app.route("/profile/create-event", methods=["POST"])
def create_event():
    try:
        data = request.json

        required_fields = ["club_name", "event_name", "description", "location"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f'Missing required field: {field}'}), 400

        club_name = data.get("club_name")
        event_name = data.get("event_name")
        description = data.get("description")
        location = data.get("location")
        img_url = data.get("img_url")

        new_event = Event(club_name=club_name, event_name=event_name, description=description, location=location, img_url=img_url)

        db.session.add(new_event)
        db.session.commit()

        return jsonify({"msg": "Event created successfully!"}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@app.route("/events/<int:id>", methods=["DELETE"])
def delete_event(id):
    try:
        event = Event.query.get(id)
        if event is None:
            return jsonify({"error": "Event not found"}), 404
        
        db.session.delete(event)
        db.session.commit()
        return jsonify({"msg": "Event deleted successfully!"}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@app.route("/events/<int:id>", methods=["PATCH"])
def update_event(id):
    try:
        event = Event.query.get(id)
        if event is None:
            return jsonify({"error": "Event not found"}), 404
        
        data = request.json

        event.event_name = data.get("event_name", event.event_name)
        event.description = data.get("description", event.description)
        event.location = data.get("location", event.location)

        db.session.commit()
        return jsonify({"msg": "Event updated successfully!"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@app.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.json

        required_fields = ["name", "password"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f'Missing required field: {field}'}), 400

        name = data.get("name")
        password = data.get("password")
        img_url = data.get("img_url")

        new_profile = Profile(name=name, img_url=img_url)
        new_profile.set_password(password)

        db.session.add(new_profile)
        db.session.commit()

        return jsonify({"msg": "Profile created successfully!"}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/signup", methods=["POST"])
def login():
    try:
        data = request.json

        name = data.get("name")
        password = data.get("password")

        if not name or not password:
            return jsonify({"error": "Name and password are required"}), 400

        user = Profile.query.filter_by(name=name).first()
        if user and user.check_password(password):
            return jsonify({"msg": "Login successful!"}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
