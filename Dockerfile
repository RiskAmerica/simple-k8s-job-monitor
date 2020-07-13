FROM python:3.6.5

ENV SLACK_WEBHOOK_URL=""
ENV CURRENT_PROJECT=""
ENV CHANNEL=""

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY src .
ENTRYPOINT ["python", "main.py"]
