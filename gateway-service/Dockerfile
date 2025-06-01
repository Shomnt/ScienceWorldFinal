FROM python:3.13

WORKDIR /gateway-service

COPY requirements.txt /gateway-service/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /gateway-service

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]