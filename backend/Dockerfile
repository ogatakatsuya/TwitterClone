FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install poetry

COPY backend/pyproject.toml backend/poetry.lock ./

ENV PYTHONPATH=/app/api

RUN poetry export -f requirements.txt --output requirements.txt
RUN pip install -r requirements.txt

ENTRYPOINT ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
