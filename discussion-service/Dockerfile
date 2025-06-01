FROM python:3.13

WORKDIR /discussion-service

COPY requirements.txt /discussion-service/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /discussion-service

EXPOSE 8003

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8003", "--reload"]