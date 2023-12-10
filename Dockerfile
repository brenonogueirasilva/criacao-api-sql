FROM python:3.10.6-slim

ENV LOCAL=False \
    PROJECT_ID=apt-theme-402300 \
    SECRET_ID=mysql-creds

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt 

COPY ./ /code

WORKDIR /code 


CMD ["sh", "-c", "python3 /code/src/data_ingestion/data_ingestion.py && uvicorn main:app --host 0.0.0.0 --port 8000"]
