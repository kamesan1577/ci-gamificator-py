#!/bin/bash

export PYTHONPATH=$PWD

cd app/db

alembic upgrade head

cd ../..

uvicorn app.main:app --reload
