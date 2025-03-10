from app import app, db
from flask import request, jsonify
from models import Event

@app.route("/api/events", methods=["GET"])
def get_events():
    events = Event.query.all()
    result = [event.to_json for event in events]
    return jsonify(result), 200

@app.route("/api/events", methods=["POST"])
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
    
@app.route("/api/events/<int:id>", methods=["DELETE"])
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
    
@app.route("/api/events/<int:id>", methods=["PATCH"])
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
