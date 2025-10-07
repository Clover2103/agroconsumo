from pydantic import BaseModel
from typing import Optional

class DatosRiego(BaseModel):
    # Datos del cultivo
    tipoCultivo: str
    etapaCultivo: str
    superficie: float

    # Condiciones del suelo
    tipoSuelo: str
    humedad: float
    retencion: Optional[float] = None
    profundidadRaiz: Optional[float] = None  # cm o m (el service lo interpreta)

    # Condiciones climáticas
    precipitacion: float
    temperatura: float
    radiacion: Optional[float] = None
    viento: Optional[float] = None
    radiacionSolar: Optional[float] = None
    velocidadViento: Optional[float] = None

    # Parámetros de gestión
    frecuencia: Optional[str] = None
    metodo: Optional[str] = None
