from fastapi import FastAPI, HTTPException, Depends, Request, Query, Body
from sqlalchemy.orm import Session
from typing import List
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse, Response

import os

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def escape_html(content: str) -> str:
    import html

    return html.escape(content)


@app.get("/")
def hello():
    return {"Hello": "World"}


@app.post("/api/test-results/", response_model=schemas.TestResult)
async def create_test_result(
    test_result: schemas.TestResultCreate, db: Session = Depends(get_db)
):
    db_test_result = crud.create_test_result(db, test_result=test_result)
    return db_test_result


@app.get("/api/test-results/", response_model=List[schemas.TestResult])
async def read_test_results(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    test_results = crud.get_test_results(db=db, skip=skip, limit=limit)
    return test_results


@app.post("/api/repositories/", response_model=schemas.Repository)
async def create_repository(
    repository: schemas.RepositoryCreate, db: Session = Depends(get_db)
):
    db_repository = crud.create_repository(db=db, repository=repository)
    return db_repository


@app.get("/api/repositories/", response_model=List[schemas.Repository])
async def read_repositories(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    repositories = crud.get_repositories(db=db, skip=skip, limit=limit)
    return repositories


@app.get("/api/repositories/{repository_id}", response_model=schemas.Repository)
async def read_repository(repository_id: int, db: Session = Depends(get_db)):
    db_repository = crud.get_repository(db=db, repository_id=repository_id)
    if db_repository is None:
        raise HTTPException(status_code=404, detail="Repository not found")
    return db_repository


@app.get("/api/developers/", response_model=List[schemas.Developer])
async def read_developers(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    developers = crud.get_developers(db=db, skip=skip, limit=limit)
    return developers


@app.get("/api/developers/{developer_name}", response_model=schemas.Developer)
async def read_developer(developer_name: str, db: Session = Depends(get_db)):
    db_developer = crud.get_developer(db=db, developer_name=developer_name)
    if db_developer is None:
        raise HTTPException(status_code=404, detail="Developer not found")
    return db_developer


@app.get("/api/leaderboard/", response_model=List[schemas.Leaderboard])
def read_leaderboard(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    leaderboard = crud.get_leaderboard(db=db, skip=skip, limit=limit)
    return leaderboard


@app.get("/leaderboard/", response_class=HTMLResponse)
async def leaderboard(request: Request, db: Session = Depends(get_db)):
    developers = crud.get_leaderboard(db=db, skip=0, limit=10)
    return templates.TemplateResponse(
        "leaderboard.html", {"request": request, "developers": developers}
    )


@app.get("/api/images/cards/{user_name}/{repo_name}", response_class=Response)
async def card(
    request: Request, user_name: str, repo_name: str, db: Session = Depends(get_db)
):
    repo = crud.get_repository_by_name(db, user_name + "/" + repo_name)
    if repo is None:
        raise HTTPException(status_code=404, detail="Repository not found")
    svg_template_response = templates.TemplateResponse(
        "card.svg",
        {"request": request, "repo": repo, "coverage": 90, "coverage_change": 10},
    )
    svg_content = svg_template_response.body
    return Response(content=svg_content, media_type="image/svg+xml")
