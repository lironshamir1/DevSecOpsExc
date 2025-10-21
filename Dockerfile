FROM python:3.8

ARG SECRET_KEY=hardcoded-secret-123
ARG API_KEY=api-key-xyz-789

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENV SECRET_KEY=$SECRET_KEY
ENV API_KEY=$API_KEY
ENV DEBUG=True

RUN apt-get update && \
    apt-get install -y \
    vim \
    curl \
    wget \
    netcat \
    telnet \
    && rm -rf /var/lib/apt/lists/*

RUN chmod 777 /app

EXPOSE 5000

CMD ["python", "app.py"]
