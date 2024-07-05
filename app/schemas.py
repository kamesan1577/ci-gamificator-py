from pydantic import BaseModel, field_validator, HttpUrl, ConfigDict
from typing import List, Optional
import datetime


class TestResultBase(BaseModel):
    developer_name: str
    code_diff: str
    coverage: float
    coverage_change: float
    repository_id: int


class TestResultCreate(TestResultBase):
    pass


class TestResult(TestResultBase):
    id: int
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class DeveloperBase(BaseModel):
    name: str


class DeveloperCreate(DeveloperBase):
    pass


class Developer(DeveloperBase):
    id: int
    total_points: int
    test_results: List[TestResult] = []

    model_config = ConfigDict(from_attributes=True)


class RepositoryBase(BaseModel):
    name: str
    url: HttpUrl

    @field_validator("url")
    def validate_github_url(cls, value):
        if "github.com" not in value:
            raise ValueError("Only GitHub repositories are allowed")
        return value


class RepositoryCreate(RepositoryBase):
    pass


class Repository(RepositoryBase):
    id: int
    test_results: List[TestResult] = []

    model_config = ConfigDict(from_attributes=True)


class Leaderboard(BaseModel):
    developer_name: str
    total_points: int
