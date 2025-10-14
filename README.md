# Order Processing Service

Servicio de ejemplo para procesamiento de órdenes en un contexto serverless y event-driven. Se construyó con **FastAPI** y **MongoDB (Motor)**, incluyendo logging estructurado, manejo de errores y simulaciones de integraciones con AWS.

## 🚀 Requisitos

- Python 3.12+
- MongoDB (local o en contenedor). Para desarrollo puedes usar Docker: `docker run -d -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=secret mongo:6`.
- (Opcional) Docker para ejecutar la aplicación containerizada.

## ▶️ Cómo ejecutar el proyecto localmente

### 1. Crear y activar un entorno virtual

El proyecto requiere Python 3.12 o superior. Utiliza la siguiente guía según tu sistema operativo:

| Sistema | Comando para crear el entorno | Comando para activarlo |
| --- | --- | --- |
| **macOS / Linux (bash/zsh)** | `python3 -m venv .venv` | `source .venv/bin/activate` |
| **Windows (PowerShell)** | `py -m venv .venv` | `.venv\\Scripts\\Activate.ps1` |
| **Windows (CMD)** | `py -m venv .venv` | `.venv\\Scripts\\activate.bat` |

> 💡 Si deseas desactivar el entorno virtual ejecuta `deactivate`.

### 2. Instalar dependencias

Con el entorno virtual activo:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Define las credenciales de MongoDB (directamente en tu shell, archivo `.env` o variables del sistema). Valores por defecto:

```env
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_DB=orders_db
MONGO_USER=root
MONGO_PASSWORD=secret
MONGO_AUTH_SOURCE=admin
LOG_LEVEL=INFO
```

### 4. Ejecutar la aplicación

Con el entorno activo y las variables configuradas, inicia el servidor de desarrollo:

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Después abre `http://localhost:8000/docs` para explorar la documentación interactiva (Swagger UI) y probar los endpoints.

### 5. Atajos mediante Makefile

Este repositorio incluye un `Makefile` que automatiza los pasos anteriores en sistemas macOS/Linux:

```bash
make venv        # Crea el entorno virtual
make install     # Instala dependencias en el entorno
make run         # Inicia el servidor de desarrollo
make test        # Ejecuta las pruebas (pytest)
make clean       # Elimina artefactos temporales y el entorno virtual
```

En Windows puedes ejecutar estos comandos dentro de Git Bash o WSL. Si prefieres PowerShell/CMD, realiza manualmente los pasos descritos en las secciones anteriores.

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
