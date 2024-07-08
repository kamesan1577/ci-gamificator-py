from sqlalchemy.orm import Session
from . import models, schemas


def create_test_result(db: Session, test_result: schemas.TestResultCreate):
    db_test_result = models.TestResult(**test_result.model_dump())
    db.add(db_test_result)
    db.commit()
    db.refresh(db_test_result)
    # ポイント計算の処理など
    developer = (
        db.query(models.Developer)
        .filter(models.Developer.name == test_result.developer_name)
        .first()
    )
    if not developer:
        developer = models.Developer(name=test_result.developer_name, total_points=0)
        db.add(developer)
        db.commit()
        db.refresh(developer)
    developer.total_points += int(
        test_result.coverage_change * 10
    )  # 例としてカバレッジの増減でポイント付与
    db.commit()
    return db_test_result


def create_repository(db: Session, repository: schemas.RepositoryCreate):
    db_repository = models.Repository(**repository.model_dump())
    db.add(db_repository)
    db.commit()
    db.refresh(db_repository)
    return db_repository


def get_test_results(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.TestResult).offset(skip).limit(limit).all()


def get_leaderboard(db: Session, skip: int = 0, limit: int = 10):
    return (
        db.query(models.Developer)
        .order_by(models.Developer.total_points.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_developers(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Developer).offset(skip).limit(limit).all()


def get_developer(db: Session, developer_name: str):
    return (
        db.query(models.Developer)
        .filter(models.Developer.name == developer_name)
        .first()
    )


def get_repositories(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Repository).offset(skip).limit(limit).all()


def get_repository(db: Session, repository_id: int):
    return (
        db.query(models.Repository)
        .filter(models.Repository.id == repository_id)
        .first()
    )


def get_repository_by_name(db: Session, repository_name: str):
    return (
        db.query(models.Repository)
        .filter(models.Repository.name == repository_name)
        .first()
    )
