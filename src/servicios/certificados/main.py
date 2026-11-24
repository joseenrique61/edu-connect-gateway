from fastapi import FastAPI, Response

app = FastAPI()


@app.get("/srv-certificados/certificados")
def get_estudiantes(response: Response):
    print("[LOG] Petición recibida en: Servicio Certificados")
    response.headers["X-Service-Name"] = "servicio-certificados"
    return {"id": 111, "estudianteId": 101}