# Deitary AI 
Web Application For Follow-Up By Nutritionist And Appointment Booking, Contains Artificial  Intelligent Suggestion System
## Installation 
1- Clone the repository:
```
git clone https://github.com/haithembenhalima/dietary_ia.git
```
2- Install dependencies:
```
pip install -r requirements.txt
```
or with
```
pip install fastapi uvicorn pydantic sqlalchemy pymysql
```
make sure that you have install `python` and `pip`
3- Create a .env file in the root directory and add the following environment variables:
```
DB_URL = "mysql+pymysql://root:@localhost:3306/nutritionist_db"
SECRET_KEY= your session secret key
```
