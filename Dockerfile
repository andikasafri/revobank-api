FROM python:3.11-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libmariadb-dev \
    pkg-config \
    wait-for-it && \
    rm -rf /var/lib/apt/lists/*

# Copy the uv binary from the external image
COPY --from=ghcr.io/astral-sh/uv:0.6.4 /uv /bin/uv

WORKDIR /flask_app

# Copy essential project files from the build context
COPY requirements.txt pyproject.toml setup.py app/.env ./

# Use bind mounts for uv.lock and pyproject.toml to run uv sync
RUN --mount=type=bind,source=uv.lock,target=/flask_app/uv.lock \
    --mount=type=bind,source=pyproject.toml,target=/flask_app/pyproject.toml \
    uv sync --frozen --no-install-project

# Copy the rest of the project files into the container
COPY . .

# Install dependencies and the project in editable mode, then install gunicorn
RUN pip install --default-timeout=100 --no-cache-dir --no-deps -r requirements.txt || true && \
    pip install --default-timeout=100 --no-cache-dir -e . && \
    pip install --default-timeout=100 --no-cache-dir gunicorn

# Copy the wait-for-it.sh script and make it executable
COPY wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh

# Set PYTHONPATH to ensure the app module can be found
ENV PYTHONPATH=/flask_app

# Use wait-for-it to pause until the MySQL container is up, then upgrade the DB and start gunicorn
CMD ["sh", "-c", "/usr/local/bin/wait-for-it.sh mysql-container:3306 -- flask db upgrade && gunicorn --bind 0.0.0.0:8000 app:app"]
