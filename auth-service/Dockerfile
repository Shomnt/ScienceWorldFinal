FROM python:3.13

WORKDIR /auth-service

COPY requirements.txt /auth-service/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /auth-service

EXPOSE 8004

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8004", "--reload"]