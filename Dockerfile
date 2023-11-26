FROM python:3.11.3-alpine

ENV PROJECT_DIR=/DirectWave
WORKDIR $PROJECT_DIR

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

WORKDIR $PROJECT_DIR/src

ENTRYPOINT ["uvicorn", "server:app"]