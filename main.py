from fastapi import FastAPI
from dotenv import load_dotenv
import os
import dotenv

from src.routes.produtos import router_produto
from src.routes.authentication import router_authentication

app = FastAPI()

load_dotenv('.env')

app.include_router(router_authentication)
app.include_router(router_produto)


