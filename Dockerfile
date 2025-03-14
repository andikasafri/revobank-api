FROM python:3.11-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libmariadb-dev \
    pkg-config \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/* && \
    ln -sf /usr/bin/nc /usr/local/bin/nc

RUN nc -h || echo "nc installation failed"

COPY --from=ghcr.io/astral-sh/uv:0.6.4 /uv /bin/uv

WORKDIR /flask_app

COPY revobank-api/requirements.txt revobank-api/pyproject.toml revobank-api/setup.py revobank-api/app/.env ./

RUN --mount=type=bind,source=revobank-api/uv.lock,target=uv.lock \
    --mount=type=bind,source=revobank-api/pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

COPY revobank-api/ .

RUN pip install --default-timeout=100 --no-cache-dir --no-deps -r requirements.txt || true && \
    pip install --default-timeout=100 --no-cache-dir -e . && \
    pip install --default-timeout=100 --no-cache-dir gunicorn

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENV PYTHONPATH=/flask_app/revobank-api

CMD ["/usr/local/bin/entrypoint.sh"]