FROM python:3.12-slim

WORKDIR /app

# Instalar system deps mínimos
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY src ./src
COPY .env ./.

# Crear usuario no root (buenas prácticas)
RUN useradd -m appuser
USER appuser

EXPOSE 8000
ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
