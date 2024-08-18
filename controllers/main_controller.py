from fastapi import Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from database import Base,SessionLocal,engine
import models
from models.analysis import Analysis
from models.user import User
import utils.crud  as crud

Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")


#Dependency
def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally:
        db.close()
        



# function to rendner the home page
def get_login_page(request: Request):
    template = 'login.html'
    context = {'request': request}
    return templates.TemplateResponse(template, context)

# fuction to render the doctor home page
def get_doctor_home_page(request: Request):
    template = '/doctor/home_doctor.html'
    doctor_id = request.session.get("doctor_id", "")
    doctor_name = request.session.get("doctor_name", "")
    context = {'request': request,"doctor_id":doctor_id,"doctor_name":doctor_name}
    return templates.TemplateResponse(template, context)

# fuction to render the doctor home page
def get_patient_home_page(request: Request):
    template = '/patient/home_patient.html'
    patient_id = request.session.get("patient_id", "")
    patient_name = request.session.get("patient_name", "")
    patient_file = request.session.get("file_name", "")
    context = {'request': request,"patient_id":patient_id,"patient_name":patient_name, "file_name": patient_file}
    return templates.TemplateResponse(template, context)


# function for the login opertation
def login_operation(db, email, password,request):
    user = crud.select_by_email(User, db, email)
    if(user):
        if(user.password == password and user.role == "doctor"):
            request.session["doctor_id"] = user.id
            request.session["doctor_name"] = user.firstname
            response = RedirectResponse(url="/doctor",status_code=302)
            return response
        elif(user.password == password and user.role == "patient"):
            request.session["patient_id"] = user.id
            request.session["patient_name"] = user.firstname
            patient_id = request.session.get("patient_id", "")
            food_data = crud.select_by_userid(Analysis, db , patient_id)
            if(food_data):
                request.session["file_name"] = food_data.max_increase
            else:
                request.session["file_name"] = "none"

            
            response = RedirectResponse(url="/patient",status_code=302)
            return response
        elif(user.password == password and user.role == "admin"):
            request.session["admin_id"] = user.id
            request.session["admin_name"] = user.firstname
            admin_id = request.session.get("admin_id", "")
            response = RedirectResponse(url="/admin",status_code=302)
            return response
        else: 
            template = "login.html"
            context = {'request': request, 'result': 'Email ou Mot passe incorrect!'}   
            return templates.TemplateResponse(template, context)

    else:
        template = "login.html"
        context = {'request': request, 'result': 'Email ou Mot passe incorrect!'}
        print(request)
        return templates.TemplateResponse(template, context)


def admin_page(request: Request, db):
    template = '/admin/admin.html'
    admin_name = request.session.get("admin_name", "")
    context = {'request': request, "admin_name": admin_name}
    return templates.TemplateResponse(template, context)

