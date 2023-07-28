FROM ubuntu:22.04

RUN apt update
RUN apt install python3.10 python3-pip -y

WORKDIR /app
COPY ./requirements_app.txt /app/requirements_app.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements_app.txt
COPY ./app .

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
