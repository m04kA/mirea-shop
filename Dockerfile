FROM python:3.7

EXPOSE 8000

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0"]