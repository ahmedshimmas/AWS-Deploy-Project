FROM python:3.12-slim AS base

WORKDIR /app

COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt



# Copy project code
FROM python:3.12-slim AS final

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY --from=base /install /usr/local

COPY . .

CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]