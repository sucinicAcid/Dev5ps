FROM python:3.11

WORKDIR /app

COPY server-collect_data/app/ ./app
COPY server-collect_data/requirements.txt .
COPY shared/ ./shared/
COPY .env .env

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

CMD ["python", "app/fetcher/main_fetch.py"]