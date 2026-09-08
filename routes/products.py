from fastapi import APIRouter,Depends,HTTPException,status,Query
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from auth import get_current_user
from schemas import ProductCreate,ProductResponse,ProductUpdate
import models

#get all products
router = APIRouter(prefix='/products',tags=['products'])
@router.get('/',response_model=list[ProductResponse])
def get_all_products(skip:int= Query(0,ge=0),
                     limit:int = Query(10,ge=1,le=20),
                     category_id:Optional[int] = None,  
                     search:Optional[str] = None,
                     db:Session = Depends(get_db)):
    query = db.query(models.Product)
    if category_id is not None:
        query = query.filter(models.Product.category_id == category_id)
    if search:
        query = query.filter(models.Product.name.ilike(f'%{search}%'))
    return query.offset(skip).limit(limit).all()

#get product by id
@router.get('/{id}', response_model=ProductResponse)
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == id).first()
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product_id:{id} not found")
    return db_product

#add product 
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
def add_product(product: ProductCreate, db: Session = Depends(get_db),current_user:models.User = Depends(get_current_user)):
    category = db.query(models.Category).filter(models.Category.id == product.category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"category_id {product.category_id} not found")

    new_product = models.Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

#update product by id
@router.put("/{id}", response_model=ProductResponse)
def update_product(id: int, product: ProductCreate, db: Session = Depends(get_db),current_user:models.User = Depends(get_current_user)):
    db_product = db.query(models.Product).filter(models.Product.id == id).first()
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product_id {id} not found")

    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.category_id = product.category_id

    db.commit()
    db.refresh(db_product)
    return db_product

@router.patch('/{id}', response_model=ProductResponse)
def partial_update_product(id: int, product: ProductUpdate, db: Session = Depends(get_db),
                            current_user: models.User = Depends(get_current_user)):
    db_product = db.query(models.Product).filter(models.Product.id == id).first()
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product_id {id} not found")

    updates = product.model_dump(exclude_unset=True)
    if "category_id" in updates:
        category = db.query(models.Category).filter(models.Category.id == updates["category_id"]).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"category_id {updates['category_id']} not found")

    for field, value in updates.items():
        setattr(db_product, field, value)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{id}")
def delete_product(id: int, db: Session = Depends(get_db),current_user:models.User = Depends(get_current_user)):
    db_product = db.query(models.Product).filter(models.Product.id == id).first()
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"product_id:{id} not found")
    db.delete(db_product)
    db.commit()
    return  f"product_id:{id} deleted"