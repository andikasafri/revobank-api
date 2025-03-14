FROM python:3.11-slim-bookworm

RUN apt-get update && apt-get install -y \
    pkg-config \
    libmariadb-dev \
    build-essential \
    gcc \
    wait-for-it

COPY --from=ghcr.io/astral-sh/uv:0.6.4 /uv /bin/uv
WORKDIR /flask_app
COPY revobank-api/requirements.txt .
COPY revobank-api/pyproject.toml .
COPY revobank-api/setup.py .
COPY revobank-api/app/.env .
RUN --mount=type=bind,source=revobank-api/uv.lock,target=uv.lock \
    --mount=type=bind,source=revobank-api/pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project
COPY revobank-api/ .
RUN pip install --no-deps -r requirements.txt || true
RUN pip install -e .
RUN pip install gunicorn

ENV PYTHONPATH=/flask_app/revobank-api

# Run migrations and start the application
CMD ["sh", "-c", "wait-for-it mysql-container:3306 -- flask db upgrade && gunicorn --bind 0.0.0.0:8000 app:app"]
