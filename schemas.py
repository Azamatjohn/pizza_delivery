from pydantic import BaseModel
from typing import Optional



class SignUpModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        orm_mode = True
        schema_extra = {
            "examples": {
                'username': 'mohirdev',
                'email': 'admin@gmail.com',
                'password': '0110',
                'is_staff': True,
                'is_active': True,
            }
        }


class SettingsModel(BaseModel):
    authjwt_secret_key: str = '58597a77ef066bb037ecaa7bc0d6e30a5b1bc6203a6b7321f5883f5084192c7a'


class LoginModel(BaseModel):
    username_or_email: str
    password: str




class OrderModel(BaseModel):
    # id: Optional[int] = None
    quantity: int
    # order_status: Optional[str] = "Pending"
    # user_id: Optional[int] = None
    product_id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "examples": {
                "quantity": 1,
                "order_status": "Pending",
                "product_id": 1,
            }
        }


class OrderStatusModel(BaseModel):
    order_status: Optional[str] = "Pending"

    class Config:
        orm_model = True
        schema_extra = {
            "examples": {
                "order_status": "Pending",
            }
        }

class OrderUpdateModel(BaseModel):
    quantity: Optional[int] = None
    product_id: Optional[int] = None
    class Config:
        orm_mode = True
        schema_extra = {
            "examples": {
                "quantity": 1,
                "product_id": 1,
                "order_status": "Pending",
            }
        }



class ProductModel(BaseModel):
    id: Optional[int] = None
    name: str
    price: int

    class Config:
        orm_mode = True
        schema_extra = {
            "examples": {
                "success": True,
                "message": "Product successfully created",
                "id": 1,
                "name": "Cheese pizza",
                "price": 10000,
            }
        }

class ProductUpdateModel(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    price: Optional[int] = None
    class Config:
        orm_mode = True
        schema_extra = {
            "examples": {
                "success": True,
                "message": "Product successfully updated",
            }
        }