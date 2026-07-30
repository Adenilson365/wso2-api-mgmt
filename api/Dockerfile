FROM python:3.10.17-alpine3.21
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
RUN chmod +x /app/start.sh
EXPOSE 8443
CMD ["/app/start.sh"]
