FROM python:3.12-alpine
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
ENTRYPOINT ["python", "bot.py"]