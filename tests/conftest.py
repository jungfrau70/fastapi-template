import os
import sys
import pytest

from fastapi.testclient import TestClient
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator
from database import Base, get_db
from config import setting
from models import User, Item
from hashing import Hasher

SQLALCHEMY_DATABASE_URL = 'sqlite:///./sqlite.db'
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
) 
TestSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

@pytest.fixture
def client():
    # Dependency Injection
    def override_get_db() -> Generator:
        db = TestSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client

@pytest.fixture
def header_token(client: TestClient):
    db = TestSessionLocal()
    user = db.query(User).filter(User.email=="user1@example.com").first()
    if user is None:
        user = User(email="user1@example.com", name="User1", hashed_password=Hasher.get_hash_password("user1"))
        db.add(user)
        db.commit()
        db.refresh(user)
    data = { "username": "user1@example.com", "password" : "user1"}
    response = client.post("/login/token", data=data)
    access_token = response.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}
