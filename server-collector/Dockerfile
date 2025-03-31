FROM python:3.10

WORKDIR /app

COPY server-collector/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server-collector/app /app/app
COPY shared /app/shared

ENV PYTHONPATH=/app

CMD ["python", "app/fetcher/main_fetch.py"]
