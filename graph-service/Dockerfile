FROM python:3.13

WORKDIR /graph-service

COPY requirements.txt /graph-service/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /graph-service

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]