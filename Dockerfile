# Use slim Python base image
FROM python:3.12-slim

# Set workdir
WORKDIR /app

# Install system dependencies for MySQL
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev gcc build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements (if you have requirements.txt or pyproject.toml)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
