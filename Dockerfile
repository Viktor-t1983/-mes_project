FROM python:3.11-slim
RUN groupadd -r mes && useradd -r -g mes mes
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y postgresql-client
RUN rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY --chown=mes:mes . .
USER mes
HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD curl -f http://localhost:8000/api/v1/health || exit 1
CMD ["python", "main.py"]
EXPOSE 8000
