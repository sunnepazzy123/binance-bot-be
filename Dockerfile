# ------------------------------
# 1️⃣ Base image
# ------------------------------
FROM python:3.12-slim

# ------------------------------
# 2️⃣ Set working directory
# ------------------------------
WORKDIR /app

# ------------------------------
# 3️⃣ Install system dependencies
# ------------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ------------------------------
# 4️⃣ Copy dependency files and README
# ------------------------------
COPY pyproject.toml uv.lock README.md ./

# ------------------------------
# 5️⃣ Install Poetry and dependencies system-wide
# ------------------------------
RUN pip install --no-cache-dir "poetry>=1.5.1" \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# ------------------------------
# 6️⃣ Copy application source code
# ------------------------------
COPY . .

# ------------------------------
# 7️⃣ Set environment variables
# ------------------------------
ENV PYTHONUNBUFFERED=1

# ------------------------------
# 8️⃣ Expose port
# ------------------------------
EXPOSE 8000

# ------------------------------
# 9️⃣ Run FastAPI
# ------------------------------
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
