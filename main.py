from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.main_routes import router as main_router
from routes.doctor_routes import router as doctor_router
from routes.patient_routes import router as patient_router
from routes.admin_routes import router as admin_router
from database import SessionLocal, engine
from starlette.middleware.sessions import SessionMiddleware
from starlette.config import Config


app = FastAPI()

#static files sources
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/pictures", StaticFiles(directory="pictures"), name="pictures")
app.mount("/analysis", StaticFiles(directory="analysis"), name="analysis")



# list of routes
app.include_router(main_router)
app.include_router(doctor_router)
app.include_router(patient_router)
app.include_router(admin_router)
config = Config(".env")
app.add_middleware(SessionMiddleware, secret_key=config("SECRET_KEY"))

#Dependency
def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally:
        db.close()