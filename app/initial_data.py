from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models


def init_db(db: Session):
    # 仮の開発者データ
    developers = [
        models.Developer(name="Alice", total_points=100),
        models.Developer(name="Bob", total_points=150),
        models.Developer(name="Charlie", total_points=200),
    ]

    # 仮のリポジトリデータ
    repositories = [
        models.Repository(name="Repo1", url="https://github.com/user/repo1"),
        models.Repository(name="Repo2", url="https://github.com/user/repo2"),
    ]

    # 仮のテスト結果データ
    test_results = [
        models.TestResult(
            developer_name="Alice",
            code_diff="diff1",
            coverage=85.0,
            coverage_change=5.0,
            repository_id=1,
        ),
        models.TestResult(
            developer_name="Bob",
            code_diff="diff2",
            coverage=90.0,
            coverage_change=10.0,
            repository_id=2,
        ),
        models.TestResult(
            developer_name="Charlie",
            code_diff="diff3",
            coverage=95.0,
            coverage_change=15.0,
            repository_id=1,
        ),
    ]

    db.add_all(developers)
    db.add_all(repositories)
    db.add_all(test_results)
    db.commit()


if __name__ == "__main__":
    db = SessionLocal()
    init_db(db)
    db.close()
