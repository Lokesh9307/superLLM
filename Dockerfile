# backend/Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY backend/ .

# Expose Flask app on port 5000
ENV PORT=5000
EXPOSE 5000

# Run the app
CMD ["python", "main.py"]
