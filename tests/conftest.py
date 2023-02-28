import os
import json
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
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

@pytest.fixture
def client():
    # Dependency Injection
    def override_get_db() -> Generator:
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client

@pytest.fixture
def header_token(client: TestClient):
    test_email = "user1@example.com"
    test_name = "User1"
    test_pass = "user1"
    db = TestingSessionLocal()
    user = db.query(User).filter(User.email==test_email).first()
    if user is None:
        user = User(email=test_email, name=test_name, hashed_password=Hasher.get_hash_password(test_pass))
        db.add(user)
        db.commit()
        db.refresh(user)
    print(user.__dict__)
    data = { "username": test_email, "password" : test_pass}
    response = client.post("/login/token", data=data)
    print(response)
    access_token = response.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}
