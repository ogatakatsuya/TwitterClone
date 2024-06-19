FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install poetry

# 依存関係ファイルを最初にコピーして Docker キャッシュを活用する
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.in-project true
RUN poetry install --no-root

# 残りのアプリケーションファイルをコピー
COPY . .

ENV PYTHONPATH=/app/api

ENTRYPOINT ["poetry", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

