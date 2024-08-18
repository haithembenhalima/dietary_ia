from fastapi import Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from database import Base,SessionLocal,engine
import models
from models.analysis import Analysis
from models.appointment import Appointment
from models.notification import Notification
from models.patient import Patient
from models.user import User
import utils.crud  as crud
import os
import shutil

Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")

UPLOAD_DIRECTORY = "pictures/profile"

#Dependency
def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally:
        db.close()


result = "" # variable to send results of requests between pages

def get_doctor_page(request: Request, db):
    global result
    template = '/doctor/account.html'
    doctor_id = request.session.get("doctor_id", "")
    # get all the data of the user 
    doctor_data = crud.select_by_id(User, db, doctor_id )
    context = {'request': request,"doctor_data":doctor_data,"result": result}
    result =""
    return templates.TemplateResponse(template, context)

def save_data(request,db,firstname,lastname,adress,wilaya,phone,email):
    doctor_id = request.session.get("doctor_id", "")
    updated_doctor_infos = crud.update_user(User,db,doctor_id,firstname,lastname,adress,wilaya,phone,email )
    response = RedirectResponse(url="/doctor/account",status_code=302)
    global result
    result = "done"
    return response

def get_picture_page(request: Request, db):
    global result
    template = '/doctor/account_picture.html'
    doctor_id = request.session.get("doctor_id", "")
    # get all the data of the user 
    doctor_data = crud.select_by_id(User, db, doctor_id )

    context = {'request': request,"doctor_data":doctor_data, "result": result}
    result =""
    return templates.TemplateResponse(template, context)

def edit_user_picture(request: Request, db,picture):
    doctor_id = request.session.get("doctor_id", "")
    file_location = os.path.join(UPLOAD_DIRECTORY, picture.filename)
    try:
        with open(file_location, "wb") as buffer:
                shutil.copyfileobj(picture.file, buffer)
    except:
         pass
    updated_picture= crud.update_picture(User,db,doctor_id, picture.filename)
    response = RedirectResponse(url="/doctor/account/picture",status_code=302)
    global result
    result = "done"
    return response

def manage_patient_page(request: Request, db):
    template = '/doctor/patient_list.html'
    doctor_id = request.session.get("doctor_id", "")
    # get all the data of the user 
    doctor_data = crud.select_by_id(User, db, doctor_id )

    patients = crud.select_by_role(User, db, "patient")

    context = {'request': request,"doctor_data":doctor_data,"patients":patients}
    return templates.TemplateResponse(template, context)
    
def add_patient_page(request: Request, db):
    global result
    template = '/doctor/add_patient.html'
    doctor_id = request.session.get("doctor_id", "")
    # get all the data of the user 
    doctor_data = crud.select_by_id(User, db, doctor_id )
    context = {'request': request,"doctor_data":doctor_data,"result": result}
    result = ""
    return templates.TemplateResponse(template, context)
    

def add_patient(request,db,firstname, lastname,password, adress, wilaya, phone, email):
    doctor_id = request.session.get("doctor_id", "")
    insert_patient = crud.insert_user(User,db,firstname, lastname,password, adress, wilaya, phone, email, doctor_id)
    response = RedirectResponse(url="/doctor/patients/add",status_code=302)
    global result
    result = "done"
    return response

def patients_infos_page(request: Request, db, patient_id):
    global result
    template = '/doctor/patient_infos.html'
    doctor_id = request.session.get("doctor_id", "")
    # get all the data of the user 
    doctor_data = crud.select_by_id(User, db, doctor_id )
    patient = crud.select_by_id(User, db, patient_id)
    patient_infos = crud.select_by_userid(Patient,db, patient_id)
    context = {'request': request,"doctor_data":doctor_data, "patient":patient,"patient_infos": patient_infos}
    result = ""
    return templates.TemplateResponse(template, context)

def validate_informations_patient(request: Request, db, patient_id):
    doctor_id = request.session.get("doctor_id", "")
    updated_doctor_infos = crud.update_patient_infos(Patient,db, patient_id,"isValide",1)
    response = RedirectResponse(url="/doctor/patients/{}".format(patient_id),status_code=302)
    global result
    result = "done"
    return response

def delete_patient_action(request: Request, db, patient_id):
    patient = crud.delete_patient(User,db, patient_id)
    patient_infos = crud.delete_patient_infos(Patient,db,patient_id)
    response = RedirectResponse(url="/doctor/patients",status_code=302)
    global result
    result = "done"
    return response

def rdv_page(request: Request, db):
    template = '/doctor/rdv.html'
    doctor_id = request.session.get("doctor_id", "")
    # get all the data of the user 
    doctor_data = crud.select_by_id(User, db, doctor_id )
    rdvs = crud.select_by_doctor_id(Appointment, db, doctor_id)
    context = {'request': request,"doctor_data":doctor_data, "rdvs": rdvs}
    return templates.TemplateResponse(template, context)

def confirm_rdv_action(request: Request, db,rdv_id):
    rdv_updated = crud.update_confirmation(Appointment,db, rdv_id,1)
    rdv = crud.select_by_id(Appointment, db, rdv_id)
    notification = crud.insert_notification(Notification, db , rdv.user_id, rdv.date, rdv.time, "Accépter")
    response = RedirectResponse(url="/doctor/rdv",status_code=302)
    global result
    result = "done"
    return response

def refuser_rdv_action(request: Request, db , rdv_id):
    rdv_updated = crud.update_confirmation(Appointment,db, rdv_id,2)
    rdv = crud.select_by_id(Appointment, db, rdv_id)
    notification = crud.insert_notification(Notification, db , rdv.user_id, rdv.date, rdv.time, "Refuser")
    response = RedirectResponse(url="/doctor/rdv",status_code=302)
    global result
    result = "done"
    return response

def analyse_page(request: Request, db):
    template = '/doctor/analysis_list.html'
    doctor_id = request.session.get("doctor_id", "")
    # get all the data of the user 
    doctor_data = crud.select_by_id(User, db, doctor_id )
    anals = crud.select_by_doctor_id(Analysis, db, doctor_id)
    context = {'request': request,"doctor_data":doctor_data, "anals": anals}
    return templates.TemplateResponse(template, context)

def analyse_page_view(request: Request, db, anal_name):
    template = '/doctor/analysis_viewer.html'
    doctor_id = request.session.get("doctor_id", "")

    context = {'request': request, "anal_name": anal_name}
    return templates.TemplateResponse(template, context)

def delete_anal_action(request: Request, db,anal_id):
    anal = crud.delete_anal(Analysis,db, anal_id)
    response = RedirectResponse(url="/doctor/analyse",status_code=302)
    global result
    result = "done"
    return response

def sys_recommand(request: Request, db):
    template = '/doctor/recommand_ia.html'
    doctor_id = request.session.get("doctor_id", "")
    # get all the data of the user 
    doctor_data = crud.select_by_id(User, db, doctor_id )
    recommnads = crud.select_by_doctor_id(Analysis, db, doctor_id)
    context = {'request': request,"doctor_data":doctor_data, "recommnads": recommnads}
    return templates.TemplateResponse(template, context)

def validate_recommand_action(request: Request, db,id):
    valid_recommand = crud.update_recommandation(Analysis,db, id, 1)
    response = RedirectResponse(url="/doctor/recommandation",status_code=302)
    global result
    result = "done"
    return response