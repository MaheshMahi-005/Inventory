from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_admin
from schemas import CategoryCreate,CategoryResponse,CategoryUpdate
import models



router = APIRouter(prefix='/categories',tags=['Categories'])

#add new category
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CategoryResponse)
def add_category(category: CategoryCreate, db: Session = Depends(get_db),current_user:models.User = Depends(get_current_admin)):
    existing = db.query(models.Category).filter(models.Category.name == category.name).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f'{category.name} already exists')
    new_category = models.Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

#get all categories
@router.get('/', response_model=list[CategoryResponse])
def get_all_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).all()

#get category by id
@router.get('/{id}',response_model=CategoryResponse)
def get_category_by_id(id:int,db:Session = Depends(get_db)):
    db_category = db.query(models.Category).filter(models.Category.id == id).first()
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'{id} not found')
    return db_category

#update category by id
@router.put('/{id}',response_model=CategoryResponse)
def update_category_by_id(id:int,category:CategoryUpdate,db:Session=Depends(get_db),current_user:models.User = Depends(get_current_admin)):
    db_category = db.query(models.Category).filter(models.Category.id == id).first()
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'category_id:{id} not found')
    db_category.name = category.name
    db.commit()
    db.refresh(db_category)
    return db_category

#delete category by id
@router.delete('/{id}')
def delete_category(id:int,db:Session =Depends(get_db),current_user:models.User = Depends(get_current_admin)):
    db_category = db.query(models.Category).filter(models.Category.id == id).first()
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'{id} not found')
    #checks any products are using category
    products = db.query(models.Product).filter(models.Product.category_id == id).count()
    if products > 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"cannot delete category '{db_category.name}': {products} product(s) still reference it")
    db.delete(db_category)
    db.commit()
    return {"detail":f'category_id:{id} deleted'}