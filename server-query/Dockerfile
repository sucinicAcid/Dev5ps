FROM python:3.11

WORKDIR /app

COPY server-query/ ./server-query
COPY shared/ ./shared/
COPY .env .env

RUN pip install --no-cache-dir -r server-query/requirements.txt

EXPOSE 8080

CMD ["uvicorn", "server-query.main_query:app", "--host", "0.0.0.0", "--port", "8080"]