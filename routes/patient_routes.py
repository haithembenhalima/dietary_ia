from fastapi import APIRouter,Request,Depends, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from database import Base,SessionLocal,engine
from controllers.patient_controller import get_patient_page, save_data,get_picture_page,edit_user_picture,patient_informations_page, save_informations_action,rdv_page,rdv_add,analyse_page,add_analyse_page, add_analyse_action,notification
from sqlalchemy.orm import Session

router = APIRouter()


#Dependency of the Database
def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally:
        db.close()


# patient edit account 
@router.get("/patient/account", response_class=HTMLResponse)
async def account_page(request: Request, db: Session = Depends(get_db)):
    return get_patient_page(request,db)

@router.post("/patient/account")
async def save_account_info(request: Request, db:Session = Depends(get_db), firstname=Form(...),lastname=Form(...),adress=Form(...),wilaya=Form(...),phone=Form(...),email=Form(...),):
    return save_data(request,db,firstname,lastname,adress,wilaya,phone,email)

@router.get("/patient/account/picture")
async def picture_page(request: Request, db: Session = Depends(get_db)):
    return get_picture_page(request,db)

@router.post("/patient/account/picture")
async def get_edit_user_picture(request: Request, db:Session = Depends(get_db),picture: UploadFile = File(...)):
    return edit_user_picture(request,db,picture)

@router.get("/patient/informations")
async def get_patient_informations_page(request: Request, db:Session = Depends(get_db)):
    return patient_informations_page(request,db)

@router.post("/patient/informations")
async def save_informations(request: Request, db:Session = Depends(get_db), age= Form(...), weight=Form(...), height= Form(...), blood_type= Form(...), disease= Form(...), drugs=Form(...) ):
    return save_informations_action(request, db , age, weight, height, blood_type,disease, drugs)

@router.get("/patient/rdv")
async def add_rdv_page(request: Request, db:Session=Depends(get_db)):
    return rdv_page(request,db)

@router.post("/patient/rdv")
async def get_rdv_add(request: Request, db:Session=Depends(get_db), date=Form(...), time=Form(...)):
    return rdv_add(request,db, date, time)

@router.get("/patient/analyse")
async def get_analyse_page(request: Request, db:Session = Depends(get_db)):
    return analyse_page(request,db)

@router.get("/patient/analyse/add")
async def get_add_analyse_page(request: Request, db:Session = Depends(get_db)):
    return add_analyse_page(request,db)

@router.post("/patient/analyse/add")
async def add_analyse_page_action(request: Request, db:Session = Depends(get_db), upload= Form(...)):
    return add_analyse_action(request,db, upload)

@router.get("/patient/notifications")
async def get_notification(request: Request, db:Session=Depends(get_db)):
    return notification(request,db)