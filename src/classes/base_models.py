from pydantic import BaseModel, EmailStr, Field
from typing import Dict, List, Optional

class ModelProduct(BaseModel):
    product_id : str = None
    product_category_name : str = None 
    product_name_lenght : Dict[str, int] = None 
    product_description_lenght : Dict[str, int] = None 
    product_photos_qty : Dict[str, int] = None
    product_weight_g : Dict[str, int] = None
    product_length_cm : Dict[str, int] = None
    product_height_cm : Dict[str, int] = None
    product_width_cm : Dict[str, int] = None
    class Config:
        schema_extra = {
            "example": {
                "product_id": "1c1890ba1779090cd54008a3c3302921",
                "product_category_name": "moveis_decoracao", 
                "product_name_lenght" : {"eq" : 27},
                "product_description_lenght" : {"eq" : 158},
                "product_photos_qty" : {"eq" : 4},
                "product_weight_g" : {"lt" : 2550},
                "product_length_cm" : {"lte" : 29},
                "product_height_cm" : {"gt" : 24},
                "product_width_cm" : {"gte" : 45}
            }
        }

class ModelProductCreate(BaseModel):
    product_id : str = None
    product_category_name : str = None 
    product_name_lenght : int = None 
    product_description_lenght : int = None 
    product_photos_qty : int = None
    product_weight_g : int = None
    product_length_cm : int = None
    product_height_cm : int = None
    product_width_cm : int = None
    class Config:
        schema_extra = {
            "example": {
                "product_id": "1c1890ba1779090cd54008a3c3302921",
                "product_category_name": "moveis_decoracao", 
                "product_name_lenght" : 27,
                "product_description_lenght" : 158,
                "product_photos_qty" : 4,
                "product_weight_g" : 2550,
                "product_length_cm" : 29,
                "product_height_cm" : 24,
                "product_width_cm" : 45
            }
        }

class ModelProductUpdate(BaseModel):
    new_register : ModelProductCreate  
    query : ModelProduct

class CreateUser(BaseModel):
    first_name: str = Field(..., description="first name user")
    last_name: str = Field(..., description="last name user")
    email: EmailStr = Field(..., description="user email")
    password: str = Field(..., description="user password") 
    class Config:
        schema_extra = {
            "example": {
                "first_name" : "Joao",
                "last_name" : "Silva",
                "email": "user@email.com",
                "password": "any_password"
            }
        }

class LoginUser(BaseModel):
    email: EmailStr = Field(..., description="user email")
    password: str = Field(..., description="user password")
    class Config:
        schema_extra = {
            "example": {
                "email": "user@email.com",
                "password": "any_password"
            }
        }
    
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
