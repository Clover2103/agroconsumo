from typing import Dict, Any
import math
from utils.constantes import (
    ROOT_ZONE_M, FIELD_CAPACITY_MM_PER_M, CROP_MAP, STAGE_MAP, SOIL_MAP,
    KC_TABLE, METHOD_EFF, PRECIP_CAT_TO_MM, AGUA_CAT_TO_M3,
    # --- NUEVAS CONSTANTES REQUERIDAS ---
    HUMEDAD_CAT_TO_PCT, RADIACION_CAT_TO_MJ_M2, VIENTO_CAT_TO_MS 
)

DEFAULT_RADIACION = 20.0
DEPLETION_FACTOR = 0.5 # fracción de agua aprovechable en el suelo
MIN_IRRIGATION_MM = 1.0 # mínimo técnico de riego sugerido (mm) cuando existe déficit pequeño


# ------------------------
# Helpers robustos para mapeo (acepta "1","1.0", 1, 1.0, etc.)
# ------------------------
def _to_key(v: Any) -> str:
    """Devuelve una clave tipo '1','2','3' cuando el valor representa un entero 1..n,
    o la representación en string por defecto."""
    if v is None:
        return ""
    try:
        if isinstance(v, (int, float)):
            return str(int(v))
        s = str(v).strip()
        if s.endswith(".0"):
            s = s[:-2]
        return s
    except Exception:
        return str(v)


def _map_inputs(data: Dict[str, Any]) -> Dict[str, Any]:
    """Normaliza y mapea entradas (acepta códigos o textos)"""
    mapped = data.copy()

    # Mapear cultivos/etapas/suelos si vienen con códigos (1/2/3) o textos
    tc_key = _to_key(mapped.get("tipoCultivo"))
    if tc_key in CROP_MAP:
        mapped["tipoCultivo"] = CROP_MAP[tc_key]

    et_key = _to_key(mapped.get("etapaCultivo"))
    if et_key in STAGE_MAP:
        mapped["etapaCultivo"] = STAGE_MAP[et_key]

    su_key = _to_key(mapped.get("tipoSuelo"))
    if su_key in SOIL_MAP:
        mapped["tipoSuelo"] = SOIL_MAP[su_key]

    # precipitacion: si viene categórica '1','2','3' -> mm
    p_key = _to_key(mapped.get("precipitacion"))
    if p_key in PRECIP_CAT_TO_MM:
        mapped["precipitacion"] = PRECIP_CAT_TO_MM[p_key]

    # agua: si viene categórica, mapear a m3
    a_key = _to_key(mapped.get("agua"))
    if a_key in AGUA_CAT_TO_M3:
        mapped["agua"] = AGUA_CAT_TO_M3[a_key]

    # --- MODIFICACIÓN CLAVE: Excluir las categorías de humedad/radiacion/viento ---
    # Convertir numerics que vengan como strings (solo los que esperamos como float)
    for k in ("superficie", "retencion", "precipitacion",
              "temperatura", "radiacion", "viento",
              "agua", "profundidadRaiz"):
        if mapped.get(k) is not None:
            try:
                mapped[k] = float(mapped[k])
            except Exception:
                # si no se puede, dejar el valor original (str, None, etc.)
                pass

    return mapped


def _get_field_capacity_mm(tipo_suelo: str, profundidad_raiz_m: float) -> float:
    """Capacidad de campo [mm] en la zona radicular (ajustada a profundidad en m)."""
    fc_per_m = FIELD_CAPACITY_MM_PER_M.get(tipo_suelo)
    if fc_per_m is None:
        fc_per_m = 120.0
    return fc_per_m * profundidad_raiz_m


def _get_kc(tipo_cultivo: str, etapa: str) -> float:
    """Obtiene Kc (fallback 0.8)."""
    return KC_TABLE.get(tipo_cultivo, {}).get(etapa, 0.8)


def _calculate_et0(temperatura: float, radiacion: float = None, viento: float = None) -> float:
    """
    Estimación de ET0 con variante Hargreaves-like.
    Incluye factor de viento como término multiplicativo simple.
    """
    rad = radiacion if (radiacion is not None) else DEFAULT_RADIACION
    wind_factor = 1.0 + ((viento or 0.0) / 10.0)  # ejemplo: viento 2 m/s -> factor 1.2
    # La radiación está en MJ/m2, la fórmula requiere una adaptación.
    # Se mantiene la lógica original, asegurando que 'rad' sea un float.
    et0 = 0.0023 * (temperatura + 17.8) * math.sqrt(rad) * wind_factor
    return et0


def _generar_recomendacion(d: dict, resultado: dict) -> dict:
    """
    Genera recomendación textual y frecuencia basada en el resultado numérico.
    Calcula también 'volumen_riego_recomendado' y 'frecuencia_riego'.
    """
    cultivo = d.get("tipoCultivo", "cultivo")
    suelo = d.get("tipoSuelo", "suelo")
    deficit = resultado.get("RequerimientoNeto_mm", 0.0)
    etc = resultado.get("ETc_mm_per_day", 0.0)
    agua_suelo_actual_mm = resultado.get("agua_suelo_actual_mm", 0.0)
    precipitacion_efectiva_mm = resultado.get("precipitacion_efectiva_mm", 0.0)

    # Estimación simple de frecuencia (días). Si etc == 0 -> 1 día por seguridad
    if etc > 0:
        dias = (agua_suelo_actual_mm * DEPLETION_FACTOR + precipitacion_efectiva_mm) / etc
        dias = max(0.5, round(dias, 1))
    else:
        dias = 1.0

    # Ajuste según tipo de suelo (arenoso pierde rápido, arcilloso retiene más)
    if suelo == "Arenoso":
        dias = max(1.0, dias - 1.0)
    elif suelo == "Franco":
        dias = max(1.0, dias)
    else:  # Arcilloso
        dias = max(1.0, dias + 1.0)

    dias = round(dias, 1)

    # Mensaje según déficit y necesidad de riego
    if resultado.get("needs_irrigation") is False:
        recomendacion = (
            f"Actualmente no se requiere riego para {cultivo}. Mantener monitoreo de humedad "
            "y revisar nuevamente si cambia el clima."
        )
    else:
        if deficit < 5:
            recomendacion = f"Riego ligero recomendado: aplicar pequeñas dosis cada {dias} días."
        elif deficit < 20:
            recomendacion = f"Riego moderado: aplicar cada {dias} días hasta recuperar niveles."
        else:
            recomendacion = f"Riego intensivo requerido: aplicar cada {dias} días hasta normalizar humedad."

    resultado.update({
        "frecuencia_riego": f"Cada {dias} días",
        "recomendacion": recomendacion
    })

    return resultado


def calcular_riego(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Cálculo principal del simulador (entrada: dict proveniente de Pydantic/data.dict()).
    Retorna diccionario con métricas y recomendaciones.
    """
    d = _map_inputs(data)

    # --- Interpretación de profundidad de raíz ---
    profundidad_input = d.get("profundidadRaiz")
    if profundidad_input is None or profundidad_input <= 0:
        profundidad_m = ROOT_ZONE_M
    else:
        # Si el usuario envía un número grande (ej 30) lo interpretamos como cm -> m
        profundidad_m = (profundidad_input / 100.0) if profundidad_input > 5.0 else profundidad_input

    superficie = float(d.get("superficie", 0.0))  # ha
    temp = float(d.get("temperatura", 0.0))
    lluvia = float(d.get("precipitacion", 0.0))  # mm
    metodo = d.get("metodo") or ""
    tipo_suelo = d.get("tipoSuelo")

    # ------------------------------------------------------------------
    # --- RECOLECCIÓN Y MAPEO DE CATEGORÍAS MODIFICADAS POR EL USUARIO ---
    # ------------------------------------------------------------------

    # 1. Humedad: Mapear la categoría ('1','2','3') al porcentaje (%)
    humedad_key = _to_key(d.get("humedad"))
    # Si viene como categoría, usa el mapa. Si falla, usar 0.0% como fallback.
    humedad_pct = HUMEDAD_CAT_TO_PCT.get(humedad_key, 0.0) 

    # 2. Radiación Solar: Mapear categoría ('1','2','3') al valor numérico (MJ/m²)
    radiacion_key = _to_key(d.get("radiacionSolar") or d.get("radiacion"))
    radiacion = RADIACION_CAT_TO_MJ_M2.get(radiacion_key, DEFAULT_RADIACION) 

    # 3. Velocidad del Viento: Mapear categoría ('1','2','3') al valor numérico (m/s)
    viento_key = _to_key(d.get("velocidadViento") or d.get("viento"))
    viento = VIENTO_CAT_TO_MS.get(viento_key, 0.0)

    # ------------------------------------------------------------------
    
    # --- Capacidad de campo (mm) ajustada a profundidad radicular ---
    capacidad_campo_mm = _get_field_capacity_mm(tipo_suelo, profundidad_m)

    # Agua presente en el suelo (mm)
    # NOTA: Se usa el valor de 'humedad_pct' mapeado o recolectado.
    agua_suelo_actual_mm = capacidad_campo_mm * (humedad_pct / 100.0)

    # Precipitación efectiva (heurística 80%)
    precipitacion_efectiva_mm = lluvia * 0.8

    # ET0 y ETc
    et0 = _calculate_et0(temp, radiacion, viento)
    kc = _get_kc(d.get("tipoCultivo"), d.get("etapaCultivo"))
    etc = et0 * kc

    # Demanda diaria antes de considerar la contribución del suelo
    demanda_mm = max(etc - precipitacion_efectiva_mm, 0.0)

    # Cuánto puede ayudar el agua en suelo (fracción aprovechable)
    mitigacion_por_suelo_mm = agua_suelo_actual_mm * DEPLETION_FACTOR

    # Requerimiento neto de riego (mm)
    requerimiento_neto_mm = max(demanda_mm - mitigacion_por_suelo_mm, 0.0)

    # Decide si se necesita riego y aplicar mínimo técnico si corresponde
    needs_irrigation = requerimiento_neto_mm > 0.0

    # Si hay un requerimiento pequeño (>0 y < MIN) aplicamos un mínimo técnico para evitar 0
    aplicable_mm = 0.0
    if not needs_irrigation:
        aplicable_mm = 0.0
    else:
        aplicable_mm = max(requerimiento_neto_mm, MIN_IRRIGATION_MM)

    # Volumen neto en m3 por ha (1 mm sobre 1 ha = 10 m3)
    volumen_neto_m3_per_ha = aplicable_mm * 10.0
    volumen_neto_m3_total = volumen_neto_m3_per_ha * superficie

    # Eficiencia del método (si viene 'metodo' usa la tabla, si no -> 0.75 por defecto)
    eficiencia = METHOD_EFF.get(metodo, 0.75)

    # Volumen bruto a aplicar teniendo en cuenta la eficiencia
    volumen_bruto_m3_per_ha = volumen_neto_m3_per_ha / eficiencia if eficiencia > 0 else volumen_neto_m3_per_ha
    volumen_bruto_m3_total = volumen_bruto_m3_per_ha * superficie

    resultado = {
        "ET0_mm_per_day": round(et0, 4),
        "Kc": round(kc, 3),
        "ETc_mm_per_day": round(etc, 4),
        "precipitacion_efectiva_mm": round(precipitacion_efectiva_mm, 3),
        "capacidad_campo_mm": round(capacidad_campo_mm, 3),
        "agua_suelo_actual_mm": round(agua_suelo_actual_mm, 3),
        "mitigacion_por_suelo_mm": round(mitigacion_por_suelo_mm, 3),
        "RequerimientoNeto_mm": round(requerimiento_neto_mm, 3),
        "aplicable_mm": round(aplicable_mm, 3),
        "VolumenNeto_m3_per_ha": round(volumen_neto_m3_per_ha, 3),
        "VolumenNeto_m3_total": round(volumen_neto_m3_total, 3),
        "Eficiencia": round(eficiencia, 3),
        "VolumenBruto_m3_per_ha": round(volumen_bruto_m3_per_ha, 3),
        "VolumenBruto_m3_total": round(volumen_bruto_m3_total, 3),
        "needs_irrigation": needs_irrigation,
    }

    # Compatibilidad con front antiguo (volumen por ha)
    resultado["volumen_riego_recomendado_m3_per_ha"] = resultado["VolumenBruto_m3_per_ha"]
    resultado["volumen_riego_recomendado_total_m3"] = resultado["VolumenBruto_m3_total"]
    # alias por compatibilidad:
    resultado["volumen_riego_recomendado"] = resultado["volumen_riego_recomendado_m3_per_ha"]

    # Añadimos recomendación y formato de salida final
    return _generar_recomendacion(d, resultado)