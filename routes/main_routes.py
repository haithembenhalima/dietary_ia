from fastapi import APIRouter,Request,Depends, Form
from fastapi.responses import HTMLResponse
from database import Base,SessionLocal,engine
from controllers.main_controller import get_login_page,get_doctor_home_page,login_operation,get_patient_home_page,admin_page
from sqlalchemy.orm import Session


router = APIRouter()


#Dependency of the Database
def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally:
        db.close()

# get the login page
@router.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return get_login_page(request)


# get the informations from the form and check it to login
@router.post("/")
async def logged_in(request: Request, db: Session = Depends(get_db), email: str = Form(...), password: str = Form(...)):
    return login_operation(db, email, password,request)

@router.get("/doctor",response_class=HTMLResponse)
async def doctor_home_page(request: Request):
    return get_doctor_home_page(request)

@router.get("/patient",response_class=HTMLResponse)
async def patient_home_page(request: Request):
    return get_patient_home_page(request)

@router.get("/admin")
async def get_admin_page(request: Request, db: Session=Depends(get_db)):
    return admin_page(request, db)


'''
@router.get("/users/")
async def get_home_page(skip:int=0, limit:int=100,db: Session = Depends(get_db) ):
    return get_users_data(db,skip,limit)

'''