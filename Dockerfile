# Use official slim Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy frozen dependencies first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Use environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Run FastAPI in production
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
