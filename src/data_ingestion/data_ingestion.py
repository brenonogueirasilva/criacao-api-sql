import pandas as pd
import os 
from dotenv import load_dotenv
import sys 


load_dotenv('.env')
local = os.getenv('LOCAL')
project_id = os.getenv('PROJECT_ID')
secret_id = os.getenv('SECRET_ID')

if local == 'True':
    sys.path.append(r'C:\Users\breno\Documents\Projetos Python\portifolio\criacao-api-local')
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] =  './creds.json'
else:
    sys.path.append('/code/') 

from src.classes.mysql import MySql
from src.classes.secret_manager import SecretManager

products_path = './src/data_ingestion/olist_products_dataset.csv'

# secret = SecretManager()
# mysql_credentials = secret.access_secret_json_file(project_id, secret_id)
# df_products = pd.read_csv(products_path)

# mysql_connector = MySql(
#     host= mysql_credentials['host'],
#     user= mysql_credentials['user'],
#     password= mysql_credentials['password'],
#     database= mysql_credentials['database']
# )


# #Table Users
# sql_drop_tabela = "drop table IF EXISTS users"
# mysql_connector.ddl_operation(sql_drop_tabela)

# sql_create_table = '''
# CREATE TABLE IF NOT EXISTS users (
#     first_name VARCHAR(255),
#     last_name VARCHAR(255),
#     email VARCHAR(255) PRIMARY KEY,
#     password VARCHAR(255)
# )
# '''
# mysql_connector.ddl_operation(sql_create_table)
# print('Table Users created')

# #Table produtos
# sql_drop_tabela = "drop table IF EXISTS produtos"
# mysql_connector.ddl_operation(sql_drop_tabela)

# sql_create_table = '''
# CREATE TABLE produtos (
#     product_id VARCHAR(255) PRIMARY KEY,
#     product_category_name VARCHAR(255),
#     product_name_lenght FLOAT,
#     product_description_lenght FLOAT,
#     product_photos_qty FLOAT,
#     product_weight_g FLOAT,
#     product_length_cm FLOAT,
#     product_height_cm FLOAT,
#     product_width_cm FLOAT
# );
# '''

# mysql_connector.ddl_operation(sql_create_table)
# mysql_connector.insert_df(df_products, 'produtos')
print('Data Ingestion with sucess')


