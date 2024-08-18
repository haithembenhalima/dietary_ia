

# select all from the database
def select_all(model, db, skip, limit):
    return db.query(model).offset(skip).limit(limit).all()

# select by email
def select_by_email(model, db, email):
    return db.query(model).filter(model.email == email).first()

# select by id
def select_by_id(model, db, id):
    return db.query(model).filter(model.id == id).first()

# select by id
def select_by_userid(model, db, user_id):
    return db.query(model).filter(model.user_id == user_id).first()

# select by id
def select_all_by_userid(model, db, user_id):
    return db.query(model).filter(model.user_id == user_id).all()

# select by role
def select_by_role(model, db, role):
    return db.query(model).filter(model.role == role).all()

# select rdv by doctor_id
def select_by_doctor_id(model, db, doctor_id):
    return db.query(model).filter(model.doctor_id == doctor_id).all()

#update user informations
def update_user(model, db, id, firstname,lastname,adress,wilaya,phone,email):
    record = db.query(model).filter(model.id == id).first()
    if record:
        record.firstname = firstname
        record.lastname = lastname
        record.adress = adress
        record.wilaya = wilaya
        record.phone = phone
        record.email = email

        db.commit()
        db.refresh(record)
    return record

def update_patient_infos(model, db,user_id, column, value):
    record = db.query(model).filter(model.user_id == user_id).first()
    if record:
        record.isValide = value
        db.commit()
        db.refresh(record)



def update_picture(model, db, id, picture):
    record = db.query(model).filter(model.id == id).first()
    if record:
        record.picture = picture
        db.commit()
        db.refresh(record)
    return record

def update_confirmation(model, db, id, confirmation):
    record = db.query(model).filter(model.id == id).first()
    if record:
        record.confirmation = confirmation
        db.commit()
        db.refresh(record)
    return record

def update_recommandation(model, db, id, recommandation_valid):
    record = db.query(model).filter(model.id == id).first()
    if record:
        record.recommandation_valid = recommandation_valid
        db.commit()
        db.refresh(record)
    return record

def insert_user(model, db,firstname, lastname,password, adress, wilaya, phone, email,doctor_id):
    new_user = model(
        firstname=firstname,
        lastname=lastname,
        adress=adress,
        wilaya=wilaya,
        phone=phone,
        email=email, 
        password= password,
        picture="user.png",
        role="patient",
        doctor_ref = doctor_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def insert_doctor(model, db,firstname, lastname,password, adress, wilaya, phone, email,doctor_id):
    new_user = model(
        firstname=firstname,
        lastname=lastname,
        adress=adress,
        wilaya=wilaya,
        phone=phone,
        email=email, 
        password= password,
        picture="user.png",
        role="doctor",
        doctor_ref = doctor_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



def insert_patient_infos(model, db , patient_id, age, weight, height, blood_type,disease, drugs, isValide):
    new_patient_infos = model(
        user_id = patient_id,
        age= age,
        weight= weight,
        height= height,
        blood_type = blood_type,
        disease=disease,
        drugs= drugs,
        isValide= isValide
    )
    db.add(new_patient_infos)
    db.commit()
    db.refresh(new_patient_infos)
    return new_patient_infos

def insert_rdv(model, db ,user_id, doctor_id, firstname, lastname, phone, date,time):
    new_rdv = model(
        user_id= user_id,
        doctor_id = doctor_id,
        firstname = firstname, 
        lastname = lastname,
        phone=phone,
        date=date,
        time=time, 
        confirmation = 0  
    )
    db.add(new_rdv)
    db.commit()
    db.refresh(new_rdv)
    return new_rdv

def insert_analyse(model, db , user_id, doctor_id,firstname, lastname, phone, pdf, max_increase, min_decrease, recommandation_valid):
    new_analyse = model(
        user_id= user_id,
        doctor_id= doctor_id,
        firstname = firstname,
        lastname = lastname, 
        phone  = phone,
        pdf = pdf, 
        max_increase =max_increase,
        min_decrease = min_decrease,
        recommandation_valid = recommandation_valid
    )
    db.add(new_analyse)
    db.commit()
    db.refresh(new_analyse)
    return new_analyse

def insert_notification(model, db , user_id,date, time, confirmation):
    new_notification = model(
        user_id= user_id,
        date = date, 
        time= time,
        confirmation = confirmation
    )
    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)
    return new_notification
def delete_patient(model, db,id):
    record = db.query(model).filter(model.id == id).first()
    if record:
        db.delete(record)
        db.commit()
    return record

def delete_patient_infos(model, db,user_id):
    record = db.query(model).filter(model.user_id == user_id).first()
    if record:
        db.delete(record)
        db.commit()
    return record

def delete_anal(model, db,anal_id):
    record = db.query(model).filter(model.id == anal_id).first()
    if record:
        db.delete(record)
        db.commit()
    return record