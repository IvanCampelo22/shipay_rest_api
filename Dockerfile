FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN chmod +x start.sh

RUN chmod +x /app/start.sh

EXPOSE 8080

USER root  

CMD ["/app/start.sh"]