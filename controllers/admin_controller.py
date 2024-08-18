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
        
result = "" # variable to send results of requests between pages

def admin_page(request: Request, db):
    template = '/admin/admin.html'
    context = {'request': request}
    return templates.TemplateResponse(template, context)

def add_page(request: Request, db):
    global result
    template = '/admin/add.html'
    admin_name = request.session.get("admin_name", "")
    context = {'request': request, "admin_name": admin_name, "result": result}
    result =""
    return templates.TemplateResponse(template, context)

def add_patient(request,db,firstname, lastname,password, adress, wilaya, phone, email):
    doctor_id = request.session.get("doctor_id", "")
    insert_patient = crud.insert_doctor(User,db,firstname, lastname,password, adress, wilaya, phone, email, 0)
    response = RedirectResponse(url="/admin/add",status_code=302)
    global result
    result = "done"
    return response



