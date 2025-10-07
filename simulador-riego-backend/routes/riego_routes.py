from fastapi import APIRouter
from models.riego_model import DatosRiego
from services.calculos_riego import calcular_riego

router = APIRouter(prefix="/api/riego", tags=["Riego"])

@router.post("/calcular")
def calcular(data: DatosRiego):
    resultado = calcular_riego(data.dict())
    return resultado
