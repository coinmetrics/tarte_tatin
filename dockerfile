FROM python:3.9-slim

WORKDIR /app

# Create an entrypoint script that will receive the Python code and execute it
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
