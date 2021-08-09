from fastapi.testclient import TestClient
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from sqlalchemy.orm import Session

from attendance.main import app, login
from attendance import crud
from attendance.database import get_db
import json

client = TestClient(app)

async def override_dependency(form_data: OAuth2PasswordRequestForm= Depends(), db:Session=Depends(get_db)):
    user_dict = crud.authenticate_user(db, account=form_data.username, passwd=form_data.password)
    return {"access_token": user_dict.account, "token_type": "bearer"}

app.dependency_overrides[login] = override_dependency

officer = {"accept": "application/json", "Authorization": "Bearer officer1", "Content-Type": "application/json"}
manager = {"accept": "application/json", "Authorization": "Bearer manager1", "Content-Type": "application/json"}
hr = {"accept": "application/json", "Authorization": "Bearer hr1", "Content-Type": "application/json"}
hr_manager = {"accept": "application/json", "Authorization": "Bearer hrmanager1", "Content-Type": "application/json"}
boss = {"accept": "application/json", "Authorization": "Bearer boss1", "Content-Type": "application/json"}

def test_create_overtime_success():
    overtime = {
        'day': '2021-08-10',
        'start': '17:00',
        'end': '19:00',
        'reason': '處理私事',
        }
    overtime_json = json.dumps(overtime)
    response = client.post("/leave", data=overtime_json, headers=officer)
    print(response.json())
    assert response.status_code == 201

def test_create_overtime_failed():
    overtime = {
        'start': '2021-08-01T08:00:23.535Z',
        'end': '2021-08-01T17:00:23.535Z',
        'category': '事假',
        'reason': '處理私事',
        'check': False
        }
    overtime_json = json.dumps(overtime)
    response = client.post("/leave", data=overtime_json, headers=officer)
    print(response.json())
    assert response.status_code == 201