FROM python:3.11-slim-bookworm

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy application code
COPY revobank-api/app/ app/
COPY revobank-api/ migrations/
COPY revobank-api/app/.env .env

# Create migrations directory if it doesn't exist
RUN mkdir -p migrations/versions

# Copy and setup entrypoint with proper line endings
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && \
    sed -i 's/\r$//' /entrypoint.sh

# Set Python path
ENV PYTHONPATH=/app

EXPOSE 8000

ENTRYPOINT ["/bin/bash"]
CMD ["/entrypoint.sh"]