from fastapi import FastAPI, Response

app = FastAPI()


@app.get("/srv-pagos/pagos")
def get_pagos(response: Response):
    print("[LOG] Petición recibida en: Servicio Pagos")
    response.headers["X-Service-Name"] = "servicio-pagos"
    return {"id": 701, "matriculaId": 501, "valor": 150.00, "estado": "PENDIENTE"}