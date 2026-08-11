from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import CategoryCreate,CategoryResponse
import models



router = APIRouter(prefix='/categories',tags=['Categories'])


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CategoryResponse)
def add_category(category: CategoryCreate, db: Session = Depends(get_db)):
    new_category = models.Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.get('/', response_model=list[CategoryResponse])
def get_all_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).all()
