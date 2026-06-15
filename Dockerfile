FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy ML module first (changes less often)
COPY machine-learning/ ./machine-learning/

# Copy backend requirements and install
COPY back-end/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy backend code
COPY back-end/ ./back-end/

WORKDIR /app/back-end

ENV ML_MODEL_PATH=/app/machine-learning
ENV FLASK_APP=run.py

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "run:app"]
