# Arquitectura serverless event-driven propuesta

## Visión general
La API residiría detrás de **Amazon API Gateway** exponiendo los endpoints REST. Cada invocación dispararía una **AWS Lambda** (imagen container) que ejecuta el servicio FastAPI. Las Lambda usan **AWS Secrets Manager** y **SSM Parameter Store** para obtener credenciales hacia **Amazon DocumentDB** o MongoDB Atlas.

## Flujo de eventos
1. **Creación de orden**: la Lambda valida la solicitud y persiste la orden. Luego publica un evento `OrderCreated` en **Amazon EventBridge**.
2. **Enriquecimiento**: una regla de EventBridge enruta el evento hacia una **AWS Step Functions** que coordina:
   - Generación de factura (Lambda dedicada) y almacenamiento en **Amazon S3**.
   - Llamadas a servicios externos (pagos, inventario) vía otras Lambdas o colas **SQS**.
3. **Actualización de estado**: cuando llega un evento de inventario/pagos, otra Lambda actualiza la orden y publica `OrderStatusChanged` en EventBridge. Esto permite fan-out hacia notificaciones (**SNS**, **SES**) o analítica (**Kinesis Firehose** → **S3/Redshift**).

## Observabilidad y gobernanza
- **CloudWatch Logs/Metrics** para recolectar logs JSON (como los que genera el proyecto) y definir alarmas (p. ej. sobre latencia o errores 5xx).
- **AWS X-Ray** o **AWS Distro for OpenTelemetry** para trazas.
- **AWS CloudTrail** y **Config** para auditoría de cambios.

## Seguridad y operación
- **API Gateway Authorizers** (JWT/Cognito) para autenticación.
- **WAF** y throttling en API Gateway para protección contra abuso.
- **IAM** mínimo privilegio para Lambdas y Step Functions.
- **Versionado** de Lambdas + **alias** para despliegues progresivos (blue/green o canary con CodeDeploy).
- **Infraestructura como código** con AWS SAM/CloudFormation/Terraform para reproducibilidad.

## Escalabilidad
- Lambdas escalan automáticamente por demanda.
- EventBridge y SQS absorben picos desacoplando productores/consumidores.
- Step Functions permite orquestar procesos largos sin servidores.
- S3 y DynamoDB/DocumentDB gestionados reducen la carga operativa.
