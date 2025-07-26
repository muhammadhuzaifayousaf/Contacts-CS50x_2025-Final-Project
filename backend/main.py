from flask import request, jsonify
from config import app, db
from models import Contact

@app.route("/contacts", methods=["GET"])
def get_contacts():
    contacts = Contact.query.all()
    json_contacts = list(map(lambda x: x.to_json(), contacts))
    return jsonify({"contacts": json_contacts})

@app.route("/create_contact", methods=["POST"])
def create_contact():
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    phone_number = request.json.get("phoneNumber")
    email = request.json.get("email")

    if not first_name or not last_name or not email or not phone_number:
        return jsonify({
            "message": "All fields are required (first name, last name, phone, email)"
        }), 400

    # Check if email exists
    if Contact.query.filter_by(email=email).first():
        return jsonify({"message": "A contact with this email already exists."}), 400

    # Check if phone number exists
    if Contact.query.filter_by(phone_number=phone_number).first():
        return jsonify({"message": "A contact with this phone number already exists."}), 400

    # Check if name already exists (regardless of phone)
    if Contact.query.filter_by(first_name=first_name, last_name=last_name).first():
        return jsonify({"message": "A contact with the same first and last name already exists."}), 400

    new_contact = Contact(
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        email=email
    )

    try:
        db.session.add(new_contact)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "User created!"}), 201


@app.route("/update_contact/<int:user_id>", methods=["PATCH"])
def update_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "User not found"}), 404

    data = request.json

    first_name = data.get("firstName")
    last_name = data.get("lastName")
    email = data.get("email")
    phone_number = data.get("phoneNumber")

    if not first_name or not last_name or not email or not phone_number:
        return jsonify({"message": "All fields are required (first name, last name, phone, email)"}), 400

    # Check if another contact has the same email
    existing_email = Contact.query.filter_by(email=email).first()
    if existing_email and existing_email.id != user_id:
        return jsonify({"message": "A contact with this email already exists."}), 400

    # Check if another contact has the same phone number
    existing_phone = Contact.query.filter_by(phone_number=phone_number).first()
    if existing_phone and existing_phone.id != user_id:
        return jsonify({"message": "A contact with this phone number already exists."}), 400

    # Check if another contact has the same name (first + last)
    existing_name = Contact.query.filter_by(first_name=first_name, last_name=last_name).first()
    if existing_name and existing_name.id != user_id:
        return jsonify({"message": "A contact with this first and last name already exists."}), 400

    # Finally, allow update
    contact.first_name = first_name
    contact.last_name = last_name
    contact.email = email
    contact.phone_number = phone_number

    db.session.commit()

    return jsonify({"message": "User updated."}), 200


@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(contact)
    db.session.commit()

    return jsonify({"message": "User deleted!"}), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
