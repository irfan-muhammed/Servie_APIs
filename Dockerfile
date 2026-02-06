FROM python:3.11-slim

WORKDIR /app

# Prevent Python from writing .pyc files and to enable unbuffered stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default port (change if your app uses a different one)
EXPOSE 8000

CMD ["python", "main.py"]
