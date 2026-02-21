FROM python:3.11-slim

WORKDIR /app

# Install minimal deps
COPY requirements.txt /app/requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && pip install --no-cache-dir -r /app/requirements.txt \
    && apt-get remove -y build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

ENV UPLOAD_DIR=/app/uploads
RUN mkdir -p ${UPLOAD_DIR}

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn","-b","0.0.0.0:8000","app:app","--workers","1"]
