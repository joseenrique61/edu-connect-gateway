from fastapi import FastAPI, Response

app = FastAPI()


@app.get("/srv-matriculas/matriculas")
def get_matriculas(response: Response):
    print("[LOG] Petición recibida en: Servicio Matrículas")
    response.headers["X-Service-Name"] = "servicio-matriculas"
    return {"id": 501, "estudianteId": 101, "estado": "ACTIVA"}