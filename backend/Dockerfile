FROM python:3.12

RUN mkdir /LifeGrid_backend

WORKDIR /LifeGrid_backend

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "src.main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker"]

