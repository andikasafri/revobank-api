FROM python:3.11-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libmariadb-dev \
    pkg-config \
    wait-for-it && \
    rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.6.4 /uv /bin/uv

WORKDIR /flask_app

COPY requirements.txt pyproject.toml setup.py .env ./

RUN --mount=type=bind,source=uv.lock,target=/flask_app/uv.lock \
    --mount=type=bind,source=pyproject.toml,target=/flask_app/pyproject.toml \
    uv sync --frozen --no-install-project

COPY . .

RUN pip install --default-timeout=100 --no-cache-dir --no-deps -r requirements.txt || true && \
    pip install --default-timeout=100 --no-cache-dir -e . && \
    pip install --default-timeout=100 --no-cache-dir gunicorn

COPY wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh

ENV PYTHONPATH=/flask_app

CMD ["sh", "-c", "/usr/local/bin/wait-for-it.sh mysql-container:3306 -- flask db upgrade && gunicorn --bind 0.0.0.0:8000 app:app"]
