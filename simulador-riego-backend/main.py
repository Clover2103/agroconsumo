from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.riego_routes import router as riego_router

app = FastAPI(title="Simulador de Control de Riego")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Ajusta según el origen de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(riego_router)

@app.get("/")
def root():
    return {"message": "API del Simulador de Riego funcionando correctamente"}
