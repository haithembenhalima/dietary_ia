from fastapi import APIRouter,Request,Depends, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from database import Base,SessionLocal,engine
from controllers.main_controller import get_login_page,get_doctor_home_page,login_operation
from controllers.doctor_controller import get_doctor_page,save_data,get_picture_page,edit_user_picture,manage_patient_page
from controllers.doctor_controller import add_patient_page,add_patient, patients_infos_page,validate_informations_patient,delete_patient_action,rdv_page
from controllers.doctor_controller import confirm_rdv_action, refuser_rdv_action,analyse_page,analyse_page_view,delete_anal_action,sys_recommand,validate_recommand_action
from sqlalchemy.orm import Session

router = APIRouter()


#Dependency of the Database
def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally:
        db.close()

# doctor edit account 
@router.get("/doctor/account", response_class=HTMLResponse)
async def account_page(request: Request, db: Session = Depends(get_db)):
    return get_doctor_page(request,db)

@router.post("/doctor/account")
async def save_account_info(request: Request, db:Session = Depends(get_db), firstname=Form(...),lastname=Form(...),adress=Form(...),wilaya=Form(...),phone=Form(...),email=Form(...),):
    return save_data(request,db,firstname,lastname,adress,wilaya,phone,email)

@router.get("/doctor/account/picture")
async def picture_page(request: Request, db: Session = Depends(get_db)):
    return get_picture_page(request,db)

@router.post("/doctor/account/picture")
async def get_edit_user_picture(request: Request, db:Session = Depends(get_db),picture: UploadFile = File(...)):
    return edit_user_picture(request,db,picture)

@router.get("/doctor/patients")
async def get_manage_patient_page(request: Request, db:Session = Depends(get_db)):
    return manage_patient_page(request,db)

@router.get("/doctor/patients/add")
async def get_add_patient_page(request: Request, db:Session = Depends(get_db)):
    return add_patient_page(request,db)

@router.post("/doctor/patients/add")
async def get_add_patient_page(request: Request, db:Session = Depends(get_db), firstname=Form(...),lastname=Form(...),adress=Form(...),wilaya=Form(...),password=Form(...),phone=Form(...),email=Form(...)):
    return add_patient(request,db,firstname, lastname,password, adress, wilaya, phone, email)

@router.get("/doctor/patients/{patient_id}")
async def get_patients_infos_page(request: Request, patient_id: int, db:Session=Depends(get_db)):
    return patients_infos_page(request, db, patient_id)

@router.post("/doctor/patients/{patient_id}")
async def validate_informations(request: Request, patient_id: int, db:Session=Depends(get_db)):
    return validate_informations_patient(request, db, patient_id)

@router.post("/doctor/patients/{patient_id}/delete")
async def delete_patient(request: Request, patient_id: int, db:Session=Depends(get_db)):
    return delete_patient_action(request, db, patient_id)

@router.get("/doctor/rdv")
async def get_rdv_page(request: Request, db:Session = Depends(get_db)):
    return rdv_page(request,db)

@router.get("/doctor/rdv/{rdv_id}/confirmer")
async def confirm_rdv(request: Request, rdv_id: int, db:Session=Depends(get_db)):
    return confirm_rdv_action(request, db, rdv_id)

@router.post("/doctor/rdv/{rdv_id}/refuser")
async def refuse_rdv(request: Request, rdv_id: int, db:Session=Depends(get_db)):
    return refuser_rdv_action(request, db, rdv_id)

@router.get("/doctor/analyse")
async def get_analyse_page(request: Request, db:Session = Depends(get_db)):
    return analyse_page(request,db)

@router.get("/doctor/analyse/{anal_name}")
async def get_analyse_page_view(request: Request, anal_name, db:Session = Depends(get_db)):
    return analyse_page_view(request,db,anal_name)

@router.post("/doctor/analyse/{anal_id}/delete")
async def delete_anal(request: Request, anal_id: int, db:Session=Depends(get_db)):
    return delete_anal_action(request, db, anal_id)

@router.get("/doctor/recommandation")
async def get_sys_recommand(request: Request, db : Session= Depends(get_db)):
    return sys_recommand(request, db)

@router.get("/doctor/recommandation/{id}")
async def validate_recommand(request: Request, id, db:Session=Depends(get_db)):
    return validate_recommand_action(request, db,id)