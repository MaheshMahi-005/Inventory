from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models
from routes import auth_routes,categories,products



app = FastAPI()
models.Base.metadata.create_all(bind=engine)


origins = ["http://localhost:5173/"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_routes.router)
app.include_router(products.router)
app.include_router(categories.router)

@app.get('/')
def greet_user():
    return {"message": "Welcome to Inventory"}