from sqlmodel import SQLModel, Field
from typing import Optional



class UserBase(SQLModel):
    user_name : str
    user_address : str
    user_email : str
    user_password : str

class User(UserBase, table=True):
    user_id: Optional[int] = Field(default=None, primary_key = True) 
