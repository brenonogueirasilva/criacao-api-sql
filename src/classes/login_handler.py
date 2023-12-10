from passlib.context import CryptContext

class LoginHandler:
    """
    A class for handling user login operations, including password hashing and verification.
    """
    def __init__(self):
        self.password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_hashed_password(self, password: str) -> str:
        """
        Hashes the provided password using the bcrypt algorithm.
        Parameters:
        - password (str): The password to be hashed.
        Returns:
        - str: The hashed password.
        """
        return self.password_context.hash(password)

    def verify_password(self, password: str, hashed_pass: str) -> bool:
        """
        Verifies if the provided password matches the hashed one.
        Parameters:
        - password (str): The password to be verified.
        - hashed_pass (str): The hashed password stored in the database.
        Returns:
        - bool: True if the passwords match, False otherwise.
        """
        return self.password_context.verify(password, hashed_pass)
    
    def generate_insert_consult(self, table_name: str, user_dict: dict) -> str:
        """
        Generates an SQL query for inserting user data into a table.
        Parameters:
        - table_name (str): The name of the table to insert data into.
        - user_dict (dict): A dictionary containing user data (first_name, last_name, email, password).
        Returns:
        - str: The SQL query for the insertion.
        """
        sql_insert = f''' 
        INSERT INTO {table_name} (first_name, last_name, email, password) 
        VALUES 
        ('{user_dict['first_name']}', 
        '{user_dict['last_name']}', 
        '{user_dict['email']}', 
        '{user_dict['password']}') 
        '''
        return sql_insert

    def generate_verify_email_consult(self, email: str, table_name: str) -> str:
        """
        Generates an SQL query to verify the existence of an email in a table.
        Parameters:
        - email (str): The email to be verified.
        - table_name (str): The name of the table to check for the email.
        Returns:
        - str: The SQL query for email verification.
        """
        sql_count = f"select count(*) from {table_name} where email = '{email}'"
        return sql_count
    
    def verify_email_return_consult(self, data_frame: pd.DataFrame) -> bool:
        """
        Verifies if the email exists based on the query result DataFrame.
        Parameters:
        - data_frame (pd.DataFrame): The DataFrame containing the result of an email verification query.
        Returns:
        - bool: True if the email exists, False otherwise.
        """
        count_lines = data_frame.iloc[0][0]
        if count_lines > 0:
            return True 
        else:
            return False
        
    def find_password_by_email_consult(self, table_name: str, email: str) -> str:
        """
        Generates an SQL query to retrieve a user's password based on their email.
        Parameters:
        - table_name (str): The name of the table to retrieve the password from.
        - email (str): The email associated with the user.
        Returns:
        - str: The SQL query for retrieving the password.
        """
        sql_count = f"select password from {table_name} where email = '{email}'"
        return sql_count