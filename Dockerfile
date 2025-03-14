FROM python:3.11-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libmariadb-dev \
    pkg-config \
    netcat-traditional \
    wait-for-it && \
    rm -rf /var/lib/apt/lists/* && \
    ln -sf /usr/bin/nc /usr/local/bin/nc

COPY --from=ghcr.io/astral-sh/uv:0.6.4 /uv /bin/uv

WORKDIR /flask_app

# Ensure the paths are correct and the files exist in the repository
COPY revobank-api/requirements.txt revobank-api/pyproject.toml revobank-api/setup.py revobank-api/app/.env ./

RUN --mount=type=bind,source=revobank-api/uv.lock,target=uv.lock \
    --mount=type=bind,source=revobank-api/pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

COPY revobank-api/ .

RUN pip install --default-timeout=100 --no-cache-dir --no-deps -r requirements.txt || true && \
    pip install --default-timeout=100 --no-cache-dir -e . && \
    pip install --default-timeout=100 --no-cache-dir gunicorn

COPY wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh

ENV PYTHONPATH=/flask_app/revobank-api

CMD ["sh", "-c", "/usr/local/bin/wait-for-it.sh mysql-container:3306 -- flask db upgrade && gunicorn --bind 0.0.0.0:8000 app:app"]
