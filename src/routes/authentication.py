
from fastapi import APIRouter, Query, HTTPException, status
import os 
from dotenv import load_dotenv

from src.classes.base_models import CreateUser, LoginUser
from src.classes.login_handler import LoginHandler
from src.classes.jwt_handler import JwtHandler
from src.classes.mysql import MySql
from src.classes.secret_manager import SecretManager

load_dotenv('.env')
local = os.getenv('LOCAL')
project_id = os.getenv('PROJECT_ID')
secret_id = os.getenv('SECRET_ID')

if local == 'True':
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] =  './creds.json' 

router_authentication = APIRouter(prefix='/authentication')
login_handler = LoginHandler()
jwt_handler = JwtHandler()

secret = SecretManager()
mysql_credentials = secret.access_secret_json_file(project_id, secret_id)


mysql_connector = MySql(
    host= mysql_credentials['host'],
    user= mysql_credentials['user'],
    password= mysql_credentials['password'],
    database= mysql_credentials['database']
)

@router_authentication.post("/signup", tags=["Authentication"], summary="Create new user")
async def create_user(user_form: CreateUser):

    select_email_count = login_handler.generate_verify_email_consult(user_form.email, 'users')
    verify_email = login_handler.verify_email_return_consult(mysql_connector.select(select_email_count))

    if verify_email:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    else:
        user_dict = {
        "first_name": user_form.first_name,
        "last_name": user_form.last_name,
        "email": user_form.email,
        "password": login_handler.get_hashed_password(user_form.password)
    }
        insert_consult = login_handler.generate_insert_consult('users', user_dict)
        mysql_connector.dml_operation(insert_consult)
        response = f"Usuario com email {user_form.email} foi criado com sucesso!"
        message = {'info' : response}
        return message

@router_authentication.post('/login', tags=["Authentication"], summary="Create access and refresh tokens for user")
async def login(form_data: LoginUser):

    select_email_count = login_handler.generate_verify_email_consult(form_data.email, 'users')
    verify_email = login_handler.verify_email_return_consult(mysql_connector.select(select_email_count))

    if not verify_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There is no Email"
        )
    else:
        password_consult = login_handler.find_password_by_email_consult('users', form_data.email)
        password_result = mysql_connector.select(password_consult).iloc[0][0]
        verify_password = login_handler.verify_password(form_data.password, password_result)
        if not verify_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect password"
            )
        response = jwt_handler.signJWT(form_data.email)
        return response