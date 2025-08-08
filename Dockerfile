FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install Poetry and Gunicorn with Uvicorn worker
RUN pip install --no-cache-dir poetry gunicorn uvicorn

# Install Python dependencies
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Ensure start.sh is executable
RUN chmod +x /app/start.sh

EXPOSE 8000
CMD ["sh", "/app/start.sh"]
