FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml README.md /app/
COPY src /app/src

RUN pip install --no-cache-dir -e .

EXPOSE 8000
ENTRYPOINT ["se-agent", "serve", "--host", "0.0.0.0", "--port", "8000"]
