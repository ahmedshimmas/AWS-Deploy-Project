FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Install Python
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt



# Copy project code
COPY . .

# Expose Django port
EXPOSE 8000

# Default command (can override in docker-compose)
CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]