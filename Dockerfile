FROM python:alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN ls -la /app && ls -la /app/app

ENTRYPOINT ["/bin/sh", "/app/entrypoint.sh"]