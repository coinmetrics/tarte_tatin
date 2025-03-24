FROM python:3.9-slim

WORKDIR /app

# Install requirements first (for better caching)
COPY requirements.txt /app/

# Install uv for dynamic dependencies
RUN pip install uv

RUN uv pip install --system -r /app/requirements.txt

# Copy entrypoint script
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Add build timestamp
RUN date > /app/build_timestamp

ENTRYPOINT ["/app/entrypoint.sh"]