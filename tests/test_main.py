import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from app.main import app, get_db
from app.db.models import Base

# テストデータベースの設定
SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides[get_db] = get_db


def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_create_test_result(client):
    response = client.post(
        "/api/test-results/",
        json={
            "developer_name": "Test Developer",
            "code_diff": "diff",
            "coverage": 90.0,
            "coverage_change": 10.0,
            "repository_id": 1,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["developer_name"] == "Test Developer"
    assert data["code_diff"] == "diff"
    assert data["coverage"] == 90.0
    assert data["coverage_change"] == 10.0
