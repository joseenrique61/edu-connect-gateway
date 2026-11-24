from fastapi import FastAPI, Response

app = FastAPI()


@app.get("/srv-estudiantes/estudiantes")
def get_estudiantes(response: Response):
    print("[LOG] Petición recibida en: Servicio Estudiantes")
    response.headers["X-Service-Name"] = "servicio-estudiantes"
    return {"id": 101, "nombre": "Ana Perez"}