from PP import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(patient_id):
    return Patient.query.get(int(patient_id))


class Patient(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    fullname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    phone = db.Column(db.Integer, unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String, nullable=False)
    generated_id = db.Column(db.Integer, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    image_file = db.Column(db.String, default='default.jpg', nullable=False)
    # is_admin = db.Column(db.Integer, default=0, nullable=False)
    appointments = db.relationship('Appointments', backref='patient_app', lazy=True)
    mydoc = db.relationship('Doctor', backref='mypatient', lazy=True)

    def __repr__(self):
        return f"Patient( 'id:{self.id}', username:{self.fullname}', 'email:{self.email}','Phone:{self.phone}')"


# done
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    belongsto = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)

    def __repr__(self):
        return f"Doctor( 'id:{self.id}', Doctor:{self.name}', 'email:{self.email}', 'whose doctor:{self.belongsto}')"


class Appointments(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    withwho = db.Column(db.String, nullable=False)
    when = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)
    # passed = None
    belongsto = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)

    def __repr__(self):
        return f"Appointments( 'id:{self.id}', Doctor:{self.withwho}', 'when:{self.when}','time:{self.time}', 'who:{self.belongsto}')"


class Medications(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    withwho = db.Column(db.String, nullable=False)
    when = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)
    # passed = None
    belongsto = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)

    def __repr__(self):
        return f"Appointments( 'id:{self.id}', Doctor:{self.withwho}', 'when:{self.when}','time:{self.time}', 'who:{self.belongsto}')"
