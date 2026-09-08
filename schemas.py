from pydantic import BaseModel
from typing  import Optional

class UserCreate(BaseModel):
    username:str
    password:str

class UserResponse(BaseModel):
    id:int
    username:str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token:str
    token_type:str


class CategoryCreate(BaseModel):
    name : str

class CategoryResponse(CategoryCreate):
    id:int

    class Config:
        from_attributes = True

class CategoryUpdate(BaseModel):
    name: str

class ProductCreate(BaseModel):
    name : str
    description : str
    price : float
    cost_price : Optional[float] = None
    category_id : int
    
class ProductResponse(BaseModel):
    id : int
    name : str
    description : str
    price : float
    category : CategoryResponse
    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    cost_price: Optional[float] = None
    category_id: Optional[int] = None