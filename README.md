# Order Processing Service

Servicio de ejemplo para procesamiento de órdenes en un contexto serverless y event-driven. Se construyó con **FastAPI** y **MongoDB (Motor)**, incluyendo logging estructurado, manejo de errores y simulaciones de integraciones con AWS.

## 🚀 Requisitos

- Python 3.12+
- MongoDB (local o en contenedor). Para desarrollo puedes usar Docker: `docker run -d -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=secret mongo:6`.
- (Opcional) Docker para ejecutar la aplicación containerizada.

## ▶️ Cómo ejecutar el proyecto localmente

1. Crear y activar un entorno virtual.
2. Instalar dependencias: `pip install -r requirements.txt`.
3. Definir variables de entorno (o crear un `.env`) con credenciales de MongoDB. Valores por defecto:
   ```env
   MONGO_HOST=localhost
   MONGO_PORT=27017
   MONGO_DB=orders_db
   MONGO_USER=root
   MONGO_PASSWORD=secret
   MONGO_AUTH_SOURCE=admin
   LOG_LEVEL=INFO
   ```
4. Ejecutar la aplicación: `uvicorn src.main:app --reload --host 0.0.0.0 --port 8000`.
5. Visitar `http://localhost:8000/docs` para la documentación interactiva generada automáticamente (Swagger UI).

### Ejecutar con Docker

```bash
docker build -t order-processing-service .
docker run --rm -p 8000:8000 \
  -e MONGO_HOST=host.docker.internal \
  -e MONGO_USER=root -e MONGO_PASSWORD=secret \
  order-processing-service
```

## 🧱 Decisiones arquitectónicas

- **Capas claras**: dominio, aplicación, infraestructura e interfaces. Favorece pruebas y reemplazo de dependencias (p. ej. otro repositorio distinto a MongoDB).
- **Motor (MongoDB async)**: permite operaciones no bloqueantes coherentes con FastAPI.
- **Logging estructurado** con `python-json-logger` para facilitar ingestión en herramientas como CloudWatch o ELK.
- **Errores de dominio** mapeados a respuestas HTTP coherentes.
- **Simulación AWS**: módulo `src/infrastructure/aws/simulated_clients.py` registra eventos que representarían interacciones con EventBridge y S3 sin requerir credenciales.

## 📈 Escalabilidad y operación en producción

- **Containerización** con Docker y despliegue en servicios como AWS Fargate, Lambda (vía container image) o Kubernetes.
- **Seguridad**: usar secretos manejados por AWS Secrets Manager, TLS extremo a extremo y autenticación/autorización (p. ej. JWT o API Gateway Authorizers).
- **Observabilidad**: enviar logs estructurados a CloudWatch, configurar métricas/paneles y trazar solicitudes con X-Ray.
- **Resiliencia**: habilitar colas/eventos (EventBridge, SQS) para desacoplar operaciones downstream y manejar reintentos.
- **Pruebas**: añadir pruebas unitarias/integración con `pytest` y pipelines CI/CD.

## 📘 Documentación API

FastAPI expone automáticamente:
- Swagger UI: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

## 📝 Arquitectura serverless event-driven

La explicación detallada se encuentra en [`docs/serverless_architecture.md`](docs/serverless_architecture.md).
