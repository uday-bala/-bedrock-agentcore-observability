FROM --platform=linux/arm64 ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy agent code
COPY s3_observability_agent.py ./

# Expose port
EXPOSE 8080

# Run application
CMD ["uvicorn", "s3_observability_agent:app", "--host", "0.0.0.0", "--port", "8080"]
