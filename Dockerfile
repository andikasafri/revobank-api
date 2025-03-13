FROM python:3.11-slim-bookworm

RUN apt-get update && apt-get install -y \
    pkg-config \
    libmariadb-dev \
    build-essential \
    gcc

COPY --from=ghcr.io/astral-sh/uv:0.6.4 /uv /bin/uv
WORKDIR /flask_app
COPY revobank-api/requirements.txt .
COPY revobank-api/pyproject.toml .
COPY revobank-api/setup.py .
RUN --mount=type=bind,source=revobank-api/uv.lock,target=uv.lock \
    --mount=type=bind,source=revobank-api/pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project
COPY revobank-api/ .
RUN pip install --no-deps -r requirements.txt || true
RUN pip install -e .
CMD ["flask", "--app", "app", "run", "--port", "8000", "--reload", "--debug", "--host", "0.0.0.0"]