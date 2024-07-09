from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
import datetime
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


class Repository(Base):
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    url = Column(String, unique=True)
    is_public = Column(Boolean, default=True)
    test_results = relationship("TestResult", back_populates="repository")

    owner_id = Column(Integer, ForeignKey("developers.id"))
    owner = relationship("Developer", back_populates="repositories")


class Developer(Base):
    __tablename__ = "developers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)  # GitHubのnameとIDって一緒なのか？
    total_points = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    test_results = relationship("TestResult", back_populates="developer")
    repositories = relationship("Repository", back_populates="owner")


class TestResult(Base):
    __tablename__ = "test_results"

    id = Column(Integer, primary_key=True, index=True)
    developer_name = Column(String, index=True)
    code_diff = Column(String)
    coverage = Column(
        Float
    )  # Jestのカバレッジがどういう形式で出力されるかわからないので、とりあえずfloatにしておく
    coverage_change = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.now)
    developer_id = Column(Integer, ForeignKey("developers.id"))
    repository_id = Column(Integer, ForeignKey("repositories.id"))

    developer = relationship("Developer", back_populates="test_results")
    repository = relationship("Repository", back_populates="test_results")
