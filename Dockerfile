# Lightweight Python image
FROM python:3.11-slim

WORKDIR /app

# Dependencies install karein
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Saara code copy karein
COPY . .

# Cloud Run ka dynamic port use karein
EXPOSE 8080
CMD ["python", "-m", "app.main"]
