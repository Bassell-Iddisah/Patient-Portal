from PP import app, bcrypt, db, gmail_user, gmail_pwd, SUBJECT
from flask import url_for, redirect, render_template, flash
from flask_login import current_user, login_user, logout_user, login_required
from PP.forms import LoginForm, RegisterForm, UpdateDetailsForm, NewAppointmentForm, MessageForm
from PP.models import Patient, Doctor
import smtplib
import secrets
import os, os.path as path
from PIL import Image


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    patient_image_file = url_for('static', filename=f'images/{current_user.fullname}/{current_user.image_file}')
    return render_template('home.html', title='Health Summary', current_user=current_user, profile=patient_image_file)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        logout_user()
    # Validate user login
    loginform = LoginForm()
    if loginform.validate_on_submit():
        generated_id = loginform.generated_id.data
        password = loginform.password.data
        patient = Patient.query.filter_by(generated_id=generated_id).first()
        if patient and bcrypt.check_password_hash(patient.password, password):
            login_user(patient, remember=loginform.remember.data)
            flash('Login Successful', 'success')
            # next = request.args.get('next')
            return redirect(url_for('home'))
        else:
            flash('either id or password wrong', 'danger')
    return render_template('login.html', loginform=loginform, current_user=current_user)


# done
@app.route('/sign_up', methods=['GET', 'POST'])
def register():
    # allow a user to register
    registerform = RegisterForm()
    if registerform.validate_on_submit():
        fullname = registerform.name.data
        email = registerform.email.data
        phone = str(registerform.phone.data)
        age = registerform.age.data
        sex = registerform.sex.data
        doc_name = registerform.doc_name.data
        doc_mail = registerform.doc_mail.data
        generated_id = secrets.token_hex(6)
        password = bcrypt.generate_password_hash(registerform.confirm_password.data)

        new_patient = Patient(fullname=fullname, email=email, phone=phone, age=age, sex=sex,
                            generated_id=generated_id, password=password)
        db.session.add(new_patient)
        db.session.commit()
        new_doctor = Doctor(name=doc_name, email=doc_mail, belongsto=new_patient.id)
        db.session.add(new_doctor)
        db.session.commit()
        send_message(TO=email, gmail_user=gmail_user
                     , gmail_pwd=gmail_pwd, SUBJECT=SUBJECT,
                     TEXT=f'''Your account has been successfully created with us.
Use your Patient ID below to sign in.

Your patient ID: {generated_id}''')


        flash(f'Account created for {fullname}, Your patient ID has been sent to your email,'
              f'please use it to log in here.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', registerform=registerform)


@app.route("/<string:id>_medications", methods=['GET', 'POST'])
@login_required
def medications(id):
    patient = Patient.query.filter_by(generated_id = id).first()
    image_file = url_for('static', filename=f'images/{patient.fullname}/{patient.image_file}')
    return render_template('medications.html', image=image_file)

# done
@app.route('/sign_out')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/<string:user_id>_appointments/", methods=['GET', 'POST'])
@login_required
def appointments(user_id):
    newform = NewAppointmentForm
    # patient = Patient.query.filter_by(generated_id=user_id).first()
    # if form.validate_on_submit():
    #     pass
    image = url_for('static', filename=f'images/doctor.jpg')
    return render_template('appointments.html', title='Patient Appointments', newform=newform, image=image)


@app.route("/<string:user_id>_account_information", methods=['GET', 'POST'])
@login_required
def account(user_id):
    form = UpdateDetailsForm()
    patient = Patient.query.filter_by(generated_id=user_id).first()
    if form.validate_on_submit():
        patient.fullname = form.name.data
        patient.email = form.email.data
        patient.phone = form.phone.data
        patient.age = form.age.data
        patient.sex = form.sex.data
        patient.image_file = save_image(form.image_file.data, patient.fullname)
        patient.password = bcrypt.generate_password_hash(form.confirm_password.data)
        db.session.commit()
        flash(f'Account updated for {patient.fullname}', 'success')
        return redirect(url_for('account', user_id=current_user.generated_id))
    image_file = url_for('static', filename=f'images/{patient.fullname}/{patient.image_file}')
    return render_template('account.html', form=form, patient=patient, image_file=image_file)


@app.route("/_account_deletion", methods=['GET', 'POST'])
@login_required
def delete_account():
    patient = Patient.query.filter_by(generated_id=current_user.generated_id).first()
    db.session.delete(patient)
    db.session.commit()
    flash('Account successfully deleted', 'success')
    return redirect(url_for('home'))


@app.route("/_contact_my_doctor", methods=['GET', 'POST'])
@login_required
def send_mail():
    mailform = MessageForm()
    patient = current_user
    if mailform.validate_on_submit():
        for doc in patient.mydoc:
            if doc.belongsto == current_user.id:
                try:
                    send_message(doc.email, gmail_user=gmail_user, gmail_pwd=gmail_pwd,
                                 SUBJECT=f'You have got mail from {current_user.fullname}',
                                 TEXT=f'Subject: {mailform.subject.data}: '
                                      f'{mailform.msg.data}')
                except Exception as e:
                    return 'Message not sent due to Error: '+str(e)
        flash('Your message has been successfully sent', 'success')
        return redirect(url_for('send_mail'))
    return render_template('reach_doctor.html', mailform=mailform)


# done
def send_message(TO, gmail_user, gmail_pwd, SUBJECT, TEXT):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        BODY = '\r\n'.join(['To: %s' % TO, 'From: %s' % gmail_user, 'Subject: %s' % SUBJECT, '', TEXT])
        server.sendmail(gmail_user, [TO], BODY)
        return "sent"
    except Exception as e:
        return "Message not sent due to Error: "+str(e)


# Get and save images submitted by forms
def save_image(picture, cat='Patients', name=None):
    # Set new picture path and new image size
    __, ext = path.splitext(picture.filename)
    new_name = f"{cat}_{name}_{secrets.token_hex(4)}{ext}"
    new_name = new_name.replace(" ", "_")
    if path.exists(f'{app.root_path}/static/images/{cat}/'):
        new_path = path.join(app.root_path, f'static/images/{cat}/{new_name}')
    else:
        os.makedirs(f'{app.root_path}/static/images/{cat}/')
        new_path = path.join(app.root_path, f'static/images/{cat}/{new_name}')
    new_size = (350, 350)
    i = Image.open(picture)
    i.thumbnail(new_size)
    i.save(new_path)
    return new_name
