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
from recommandation_sys.mixt import recommand

Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")

UPLOAD_DIRECTORY = "analysis/"
result = "" # variable to send results of requests between pages

def get_patient_page(request: Request, db):
    global result
    template = '/patient/account.html'
    patient_id = request.session.get("patient_id", "")
    # get all the data of the user 
    patient_data = crud.select_by_id(User, db, patient_id )
    context = {'request': request,"patient_data":patient_data,"result": result}
    result =""
    return templates.TemplateResponse(template, context)

def save_data(request,db,firstname,lastname,adress,wilaya,phone,email):
    patient_id = request.session.get("patient_id", "")
    updated_patient_infos = crud.update_user(User,db,patient_id,firstname,lastname,adress,wilaya,phone,email )
    response = RedirectResponse(url="/patient/account",status_code=302)
    global result
    result = "done"
    return response

def get_picture_page(request: Request, db):
    global result
    template = '/patient/account_picture.html'
    patient_id = request.session.get("patient_id", "")
    # get all the data of the user 
    patient_data = crud.select_by_id(User, db, patient_id )

    context = {'request': request,"patient_data":patient_data, "result": result}
    result =""
    return templates.TemplateResponse(template, context)

def edit_user_picture(request: Request, db,picture):
    patient_id = request.session.get("patient_id", "")
    file_location = os.path.join(UPLOAD_DIRECTORY, picture.filename)
    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(picture.file, buffer)
    except:
        pass
    updated_picture= crud.update_picture(User,db,patient_id, picture.filename)
    response = RedirectResponse(url="/patient/account/picture",status_code=302)
    global result
    result = "done"
    return response

def patient_informations_page(request: Request, db):
    global result
    template = '/patient/informations.html'
    patient_id = request.session.get("patient_id", "")
    # get all the data of the user 
    patient_data = crud.select_by_id(User, db, patient_id )
    informations = crud.select_by_userid(Patient, db, patient_id)
    context = {'request': request,"patient_data":patient_data,"result": result, "infos": informations}
    result =""
    return templates.TemplateResponse(template, context)

def save_informations_action(request, db , age, weight, height, blood_type,disease, drugs):
    patient_id = request.session.get("patient_id", "")
    updated_patient_infos = crud.insert_patient_infos(Patient,db,patient_id,age, weight, height, blood_type,disease, drugs,0)
    response = RedirectResponse(url="/patient/informations",status_code=302)
    global result
    result = "done"
    return response

def rdv_page(request, db):
    global result
    template = '/patient/rdv.html'
    patient_id = request.session.get("patient_id", "")
    # get all the data of the user 
    patient_data = crud.select_by_id(User, db, patient_id )
    context = {'request': request,"patient_data":patient_data,"result": result}
    result =""
    return templates.TemplateResponse(template, context)

def rdv_add(request, db , date, time):
    patient_id = request.session.get("patient_id", "")
    patient_data = crud.select_by_id(User, db , patient_id )
    rdv = crud.insert_rdv(Appointment,db,patient_id,patient_data.doctor_ref, patient_data.firstname, patient_data.lastname, patient_data.phone, date, time )
    response = RedirectResponse(url="/patient/rdv",status_code=302)
    global result
    result = "done"
    return response

def analyse_page(request: Request, db):
    template = '/patient/analysis_list.html'
    patient_id = request.session.get("patient_id", "")
    # get all the data of the user 
    patient_data = crud.select_by_id(User, db, patient_id )
    anals = crud.select_all_by_userid(Analysis, db, patient_id)
    context = {'request': request,"patient_data":patient_data, "anals": anals}
    return templates.TemplateResponse(template, context)


def add_analyse_page(request: Request, db):
    global result
    template = '/patient/add_analysis.html'
    patient_id = request.session.get("patient_id", "")
    # get all the data of the user 
    patient_data = crud.select_by_id(User, db, patient_id )
    context = {'request': request,"patient_data":patient_data,"result": result}
    return templates.TemplateResponse(template, context)

def add_analyse_action(request: Request, db , upload):
    patient_id = request.session.get("patient_id", "")
    patient_data = crud.select_by_id(User, db, patient_id)
    file_location = os.path.join(UPLOAD_DIRECTORY, upload.filename)
    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(upload.file, buffer)
    except:
         pass
    
    # call the IA model to to recommandation for the analyse pdf file      
    recommand(upload.filename)
    # result of the recommandation sys
    file = upload.filename
    base_name = file.replace('.pdf', '')
    max_increase = base_name+"_comparison_increase.csv"
    min_decrease = base_name+"_comparison_decrease.csv"
    # save the data in the db
    new_analyse = crud.insert_analyse(Analysis, db , patient_id, patient_data.doctor_ref,patient_data.firstname, patient_data.lastname, patient_data.phone, upload.filename,max_increase, min_decrease, 0 )
    response = RedirectResponse(url="/patient/analyse/add",status_code=302)
    global result
    result = "done"
    return response 

def notification(request: Request, db):
    template = '/patient/notification.html'
    patient_id = request.session.get("patient_id", "")
    # get all the data of the user 
    patient_data = crud.select_by_id(User, db, patient_id )
    notifs = crud.select_all_by_userid(Notification, db, patient_id)
    context = {'request': request,"patient_data":patient_data, "notifs": notifs}
    return templates.TemplateResponse(template, context)