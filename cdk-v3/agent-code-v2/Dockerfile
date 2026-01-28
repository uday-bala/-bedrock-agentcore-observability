FROM --platform=linux/arm64 ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy agent code
COPY toolkit_style_agent.py ./

# Expose port
EXPOSE 8080

# Run application with OpenTelemetry auto-instrumentation
CMD ["opentelemetry-instrument", "python", "toolkit_style_agent.py"]
