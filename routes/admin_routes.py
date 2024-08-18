from fastapi import APIRouter,Request,Depends, Form
from fastapi.responses import HTMLResponse
from database import Base,SessionLocal,engine
from controllers.admin_controller import admin_page,add_page,add_patient
from sqlalchemy.orm import Session


router = APIRouter()


#Dependency of the Database
def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally:
        db.close()

@router.get("/admin")
async def get_admin_page(request: Request, db: Session=Depends(get_db)):
    return admin_page(request, db)

@router.get("/admin/add")
async def get_add_page(request: Request, db: Session=Depends(get_db)):
    return add_page(request, db)

@router.post("/admin/add")
async def get_add_patient_page(request: Request, db:Session = Depends(get_db), firstname=Form(...),lastname=Form(...),adress=Form(...),wilaya=Form(...),password=Form(...),phone=Form(...),email=Form(...)):
    return add_patient(request,db,firstname, lastname,password, adress, wilaya, phone, email)