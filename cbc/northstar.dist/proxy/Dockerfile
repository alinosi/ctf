FROM python:3.12-alpine

WORKDIR /app

COPY proxy/proxy.py /app/proxy.py

EXPOSE 8080

ENV PROXY_HOST=0.0.0.0
ENV PROXY_PORT=8080

CMD ["python", "/app/proxy.py"]
