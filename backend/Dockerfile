FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /app/backend

RUN pip install poetry

COPY ./backend/pyproject.toml ./backend/poetry.lock /app/

RUN poetry config virtualenvs.in-project true

RUN poetry install --no-dev

COPY . /app

ENTRYPOINT ["poetry", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--reload"]