from fastapi import FastAPI
from config import setting
from database import engine
from models import Base
from routers import users, items, login
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(engine)

tags = [
    {
        "name": "user",
        "description": "These are my user related routes"
    },
    {
        "name": "product",
        "description": "There are my product related routes"
    }
]
    
app = FastAPI(
    title = setting.TITLE,
    description = setting.DESCRIPTION,
    version = setting.VERSION,
    contact = {
        "name": setting.NAME,
        "email": setting.EMAIL,
    },
    openapi_tages = tags,
    openapi_url = "/api/v1/openapi.json",
    # docs_url = "/documentation",
    redoc_url = None
    )

@app.get('/getenvvar', tags=["config"]) #, prefix="/product")
def get_envvars():
    return {"database": setting.DATABASE_URL }


app.include_router(users.router)
# app.include_router(items.router)
# app.include_router(login.router)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
