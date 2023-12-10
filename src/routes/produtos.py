from fastapi import APIRouter, Query, Depends, Request
import pandas as pd 
from typing import Dict, List
import os
from dotenv import load_dotenv

from src.classes.auth_bearer import AuthBearer 
from src.classes.mysql import MySql
from src.classes.base_models import ModelProduct, ModelProductCreate, ModelProductUpdate
from src.classes.integrate_api_database import IntegrateApiDataBase
from src.classes.secret_manager import SecretManager

load_dotenv('.env')
local = os.getenv('LOCAL')
project_id = os.getenv('PROJECT_ID')
secret_id = os.getenv('SECRET_ID')

if local == 'True':
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] =  './creds.json' 


secret = SecretManager()
mysql_credentials = secret.access_secret_json_file(project_id, secret_id)


mysql_connector = MySql(
    host= mysql_credentials['host'],
    user= mysql_credentials['user'],
    password= mysql_credentials['password'],
    database= mysql_credentials['database']
)
integrate_api = IntegrateApiDataBase()
router_produto = APIRouter(prefix='/produtos')

table_name = 'produtos'

@router_produto.get("/select", tags=["Produtos"], summary="Select Produtos" ) #, dependencies= [Depends(AuthBearer())])
async def select_api( 
    page: int = Query(1, description='Numero da pagina', ge=1), 
    page_size: int = Query(10, description='Quantidade itens por pagina', ge=5, le=100),
    product_category_name: str =  Query('product_category_name', description='Suportado Parametro Map, parametro.lt=27'),
    product_name_lenght : str =  Query('product_name_lenght', descripition='Suportado Parametro Map, parametro.lt=27'), 
    product_description_lenght: str = Query('product_description_lenght', descripition='Suportado Parametro Map, parametro.lt=27'),
    product_photos_qty: str = Query('product_photos_qty', descripition='Suportado Parametro Map, parametro.lt=27'), 
    product_weight_g: str = Query('product_weight_g', descripition='Suportado Parametro Map, parametro.lt=27'),
    product_length_cm: str = Query('product_length_cm', descripition='Suportado Parametro Map, parametro.lt=27'), 
    product_height_cm: str = Query('product_height_cm', descripition='Suportado Parametro Map, parametro.lt=27'),
    product_width_cm: str = Query('product_width_cm', descripition='Suportado Parametro Map, parametro.lt=27')
    ):
    dict_parameters = {
        'product_category_name' : product_category_name,
        'product_name_lenght' : product_name_lenght,
        'product_description_lenght' : product_description_lenght,
        'product_photos_qty' : product_photos_qty,  
        'product_weight_g' : product_weight_g,
        'product_length_cm' : product_length_cm,
        'product_height_cm' : product_height_cm,
        'product_width_cm' : product_width_cm
    }
    dict_params = integrate_api.convert_get_params_to_format_dict(dict_parameters)
    sql_select = integrate_api.generate_select(table_name, dict_params, page, page_size)
    sql_select_count = integrate_api.generate_select_count(table_name, dict_params)

    data_frame = mysql_connector.select(sql_select)
    count_registers = int(mysql_connector.select(sql_select_count).iloc[0][0])

    response = integrate_api.generate_response_paginate(data_frame, page, page_size, count_registers)
    return response

# @router_produto.post("/select", tags=["Produtos"], summary="Select Produtos" ) #, dependencies= [Depends(AuthBearer())])
# async def select_api(
#     params : ModelProduct,
#     page: int = Query(1, description='Numero da pagina', ge=1), 
#     page_size: int = Query(10, description='Quantidade itens por pagina', ge=5, le=100)
#     ):

#     dict_params = integrate_api.params_to_dict(params)
#     sql_select = integrate_api.generate_select(table_name, dict_params, page, page_size)
#     sql_select_count = integrate_api.generate_select_count(table_name, dict_params)

#     data_frame = mysql_connector.select(sql_select)
#     count_registers = int(mysql_connector.select(sql_select_count).iloc[0][0])
#     response = integrate_api.generate_response_paginate(data_frame, page, page_size, count_registers)
#     return response


@router_produto.delete("/delete", tags=["Produtos"], summary="Delete Produtos"  , dependencies= [Depends(AuthBearer())])
async def delete_api(
    params : ModelProduct
    ):
    dict_params = integrate_api.params_to_dict(params)

    sql_select_count = integrate_api.generate_select_count(table_name, dict_params)
    count_registers = int(mysql_connector.select(sql_select_count).iloc[0][0])
    message = f"Registers Deleted: {count_registers}"

    sql_delete = integrate_api.generate_delete(table_name, dict_params)
    mysql_connector.dml_operation(sql_delete)
    return message

@router_produto.post("/create", tags=["Produtos"], summary="Create Produtos" , dependencies= [Depends(AuthBearer())])
async def create_api(
    ls_params : List[ModelProductCreate]
    ):
    ls_dicts = integrate_api.list_params_to_dict(ls_params)
    dataframe_insert = pd.DataFrame(ls_dicts)

    mysql_connector.insert_df(dataframe_insert, table_name)
    message = f"Registers Inserted : {len(ls_dicts)}"
    return message

@router_produto.put("/put", tags=["Produtos"], summary="Update Produtos"  , dependencies= [Depends(AuthBearer())])
async def update_api(
    params : ModelProductUpdate
    ):
    new_register = params.new_register
    dict_params = integrate_api.params_to_dict(new_register)
    dict_query = integrate_api.params_to_dict( params.query)

    sql_update = integrate_api.generate_update(table_name, dict_params, dict_query)
    mysql_connector.dml_operation(sql_update)

    sql_select_count = integrate_api.generate_select_count(table_name, dict_query)
    count_registers = int(mysql_connector.select(sql_select_count).iloc[0][0])
    message = f"Registers Updated: {count_registers}"

    return message
