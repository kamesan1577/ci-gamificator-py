from sqlalchemy.orm import Session
from database import SessionLocal, engine
from app.db import models


def reset_db():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)


def init_db(db: Session):
    # 仮の開発者データ
    developers = [
        models.Developer(name="alice", total_points=100),
        models.Developer(name="bob", total_points=150),
        models.Developer(name="charlie", total_points=200),
    ]

    # 仮のリポジトリデータ
    repositories = [
        models.Repository(name="alice/repo1", url="https://github.com/alice/repo1"),
        models.Repository(name="bob/repo2", url="https://github.com/bob/repo2"),
    ]

    # 仮のテスト結果データ
    test_results = [
        models.TestResult(
            developer_name="alice",
            code_diff="diff1",
            coverage=85.0,
            coverage_change=5.0,
            repository_id=1,
        ),
        models.TestResult(
            developer_name="bob",
            code_diff="diff2",
            coverage=90.0,
            coverage_change=10.0,
            repository_id=2,
        ),
        models.TestResult(
            developer_name="charlie",
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
    reset_db()
    db = SessionLocal()
    init_db(db)
    db.close()
