# EduConnect API Gateway — Kong DB-Less - Grupo 1

Este repositorio contiene la infraestructura y los microservicios mock para la plataforma **EduConnect**. La solución utiliza **Kong API Gateway (en modo DB-less)** para centralizar el enrutamiento, la autenticación y las políticas de limitación de tasa (*rate limiting*) sobre cuatro microservicios independientes construidos con **FastAPI**.

---

## 1. Requisitos Previos

Antes de desplegar el entorno, asegúrate de tener instalado:

* [Docker Engine](https://docs.docker.com/engine/install/) (v20.10 o superior)
* [Docker Compose](https://docs.docker.com/compose/) (v2.0 o superior)
* [cURL](https://curl.se/) (para pruebas desde terminal)
* [Postman](https://www.postman.com/) (para ejecutar las pruebas automatizadas)

---

## 2. Versiones Elegidas y Tecnologías

* **API Gateway:** `kong/kong:3.9.5` (Configuración declarativa DB-less, formato `_format_version: "3.0"`).
* **Backends:** Python `3.11-slim` con frameworks **FastAPI** y servidor ASGI **Uvicorn**.
* **Orquestación:** Docker Compose v3.8.
* **Red:** Red interna puente (`kong-net`).

---

## 3. Arquitectura y Mapeo de URLs

Los microservicios se encuentran aislados dentro de la red Docker (`kong-net`) y únicamente son accesibles a través del puerto proxy de Kong (`8000`).

| Servicio | URL Pública (Kong Gateway) | Upstream Interno (Docker) | Método | Política Rate Limit |
|---|---|---|---|---|
| **Estudiantes** | `http://localhost:8000/api/estudiantes` | `http://srv-estudiantes:8000/srv-estudiantes/estudiantes` | GET | 5 req/min (Consumidor) |
| **Matrículas** | `http://localhost:8000/api/matriculas` | `http://srv-matriculas:8000/srv-matriculas/matriculas` | GET | 5 req/min (Consumidor) |
| **Pagos** | `http://localhost:8000/api/pagos` | `http://srv-pagos:8000/srv-pagos/pagos` | GET | 5 req/min (Consumidor) |
| **Certificados** | `http://localhost:8000/api/certificados` | `http://srv-certificados:8000/srv-certificados/certificados` | GET | **2 req/min** (Específico) |

### Credenciales y Políticas Configuradas
* **Autenticación (`key-auth`):** Global para todos los endpoints mediante el header `apikey`.
* **Consumidor:** `cliente-app`
* **API Key:** `edu-connect-secret-key`
* **Precedencia de Rate Limiting:**
  * General para `cliente-app`: **5 peticiones / minuto**.
  * Específico para `cliente-app` en `/api/certificados`: **2 peticiones / minuto** (evaluado con prioridad por la regla `Consumer + Service`).

---

## 4. Instrucciones de Arranque

1. Clona el repositorio y sitúate en el directorio `src/`:
    ```bash
    git clone https://github.com/joseenrique61/edu-connect-gateway && cd edu-connect-gateway/src/
    ```
2. Construye las imágenes y levanta los contenedores en segundo plano:
   ```bash
   docker compose up --build -d
   ```
3. Verifica que los 5 contenedores estén en estado *Up*:
   ```bash
   docker compose ps
   ```
4. (Opcional) Monitorea los logs en vivo:
   ```bash
   docker compose logs -f
   ```

---

## 5. Pruebas y Validación

La carpeta `./postman` incluye la colección **`EduConnectGateway`** con 8 casos de prueba que evalúan los escenarios de éxito, seguridad y control de errores en Kong.

### Casos de Prueba Incluidos:

1. **`Estudiantes`**: Valida respuesta exitosa (`200 OK`), datos del estudiante y cabecera `X-Service-Name: servicio-estudiantes`.
2. **`Matriculas`**: Valida respuesta exitosa (`200 OK`), datos de matrícula y cabecera `X-Service-Name: servicio-matriculas`.
3. **`Pagos`**: Valida respuesta exitosa (`200 OK`), datos de pago y cabecera `X-Service-Name: servicio-pagos`.
4. **`Certificados`**: Valida respuesta exitosa (`200 OK`) o `429 Too Many Requests` según la cuota de rate limiting.
5. **`Estudiantes - Sin API Key`**: Valida que Kong bloquee la petición con `401 Unauthorized` si no se envía la cabecera `apikey`.
6. **`Estudiantes - API Key Incorrecta`**: Valida que Kong devuelva `401 Unauthorized` si la API Key proporcionada no existe.
7. **`Ruta No Existente`**: Solicita `/api/clases` y valida que Kong responda con `404 Not Found` (`no Route matched with those values`).
8. **`Certificados - Rate Limit Excedido`**: Valida que Kong bloquee más de 2 requests por minuto en el servicio de Certificados con `429 Too Many Requests`.

---

### Cómo Ejecutar las Pruebas

1. Abre Postman e importa el archivo `./postman/EduConnectGateway.json`.
2. Asegúrate de que la variable de colección `baseUrl` tenga el valor `http://localhost:8000`.
3. Haz clic derecho sobre la colección y selecciona **Run**.
4. Haz clic en **Start Run**. Todos los tests automáticos deben pasar en verde.

---

## 6. Instrucciones para Detener la Solución

Para detener los contenedores y remover la red compartida:
```bash
docker compose down
```

Para detener la solución eliminando además los volúmenes temporales de Kong (`kong-tmp`, `kong-prefix`):
```bash
docker compose down -v
```