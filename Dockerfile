FROM python:3.12
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/src

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install base dependencies
RUN pip install -U pip poetry gunicorn uvicorn[standard]

# Install dependencies
COPY ./pyproject.toml ./poetry.lock ./README.md /tmp/
RUN cd /tmp && poetry config virtualenvs.create false && poetry install --no-interaction --only=main

# Copy code
WORKDIR /src
COPY ./src/ /src
# COPY ./key.json /src/key.json
COPY ./deployment/gunicorn_config.py /src

EXPOSE 8080
ENTRYPOINT ["gunicorn","-k","uvicorn.workers.UvicornWorker","-b", "0.0.0.0:8080", "main:app"]
