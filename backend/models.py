from config import db

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(80), unique = False, nullable = False)
    last_name = db.Column(db.String(80), unique = False, nullable = False)
    phone_number = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(120), unique = True, nullable = False)

    def to_json(self):
        return {
            "id" : self.id,
            "firstName" : self.first_name,
            "lastName" : self.last_name,
            "phoneNumber": self.phone_number,
            "email" : self.email,
        }