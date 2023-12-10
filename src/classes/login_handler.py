from passlib.context import CryptContext

class LoginHandler:
    def __init__(self):
        self.password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_hashed_password(self, password: str) -> str:
        return self.password_context.hash(password)

    def verify_password(self, password: str, hashed_pass: str) -> bool:
        return self.password_context.verify(password, hashed_pass)
    
    def generate_insert_consult(self, table_name, user_dict):
        sql_insert = f''' 
        INSERT INTO {table_name} (first_name, last_name, email, password) 
        VALUES 
        ('{user_dict['first_name']}', 
        '{user_dict['last_name']}', 
        '{user_dict['email']}', 
        '{user_dict['password']}') 
        '''
        return sql_insert

    def generate_verify_email_consult(self, email, table_name):
        sql_count = f"select count(*) from {table_name} where email = '{email}'"
        return sql_count
    
    def verify_email_return_consult(self, data_frame):
        count_lines = data_frame.iloc[0][0]
        if count_lines > 0:
            return True 
        else:
            return False
        
    def find_password_by_email_consult(self, table_name, email):
        sql_count = f"select password from {table_name} where email = '{email}'"
        return sql_count