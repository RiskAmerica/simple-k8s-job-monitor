FROM python:3.6.5

ENV SLACK_WEBHOOK_URL=""
ENV CURRENT_PROJECT=""
ENV CHANNEL=""

WORKDIR /app

COPY src .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]
