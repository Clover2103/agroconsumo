# Profundidad radicular (m)
ROOT_ZONE_M = 0.30

# Capacidad de campo (mm por m de profundidad)
FIELD_CAPACITY_MM_PER_M = {
    "Arenoso": 60,
    "Arcilloso": 200,
    "Franco": 150,
    "1": 60,
    "2": 200,
    "3": 150,
}

# Mapas de equivalencias
CROP_MAP = {"1": "Maíz", "2": "Arroz", "3": "Café"}
# --- CAMBIO 1: SE AÑADE FLORACIÓN (clave "2") ---
STAGE_MAP = {"1": "Siembra", "2": "Floración", "3": "Crecimiento", "4": "Cosecha"}
SOIL_MAP = {"1": "Arenoso", "2": "Arcilloso", "3": "Franco"}

# Coeficiente de cultivo (Kc)
# --- CAMBIO 2: SE AÑADE KC PARA FLORACIÓN (se mantiene la coherencia) ---
KC_TABLE = {
    "Maíz": {"Siembra": 0.4, "Floración": 1.15, "Crecimiento": 0.9, "Cosecha": 0.6},
    "Arroz": {"Siembra": 1.1, "Floración": 1.15, "Crecimiento": 1.2, "Cosecha": 0.9},
    "Café": {"Siembra": 0.5, "Floración": 1.0, "Crecimiento": 0.8, "Cosecha": 0.7},
}

# Eficiencias por método de riego
METHOD_EFF = {
    "Goteo": 0.90,
    "Aspersión": 0.75,
    "Surcos": 0.60,
    "Inundación": 0.50,
    "Pivot central": 0.65,
}

# --- NUEVOS MAPAS HEURÍSTICOS ---

# Precipitación (se asume que las categorías '1','2','3' siguen siendo Baja/Media/Alta)
PRECIP_CAT_TO_MM = {"1": 5.0, "2": 20.0, "3": 50.0}
AGUA_CAT_TO_M3 = {"1": 1000.0, "2": 5000.0, "3": 10000.0}

# --- CAMBIO 3: Mapa de Humedad del Suelo a % (o factor de corrección) ---
# En tu lógica actual usas "humedad_pct = float(d.get("humedad", 0.0))",
# lo que indica que el valor enviado desde el front es el porcentaje.
# Ya que el front ahora envía códigos ('1', '2', '3'), debemos mapear esos códigos a un porcentaje.
HUMEDAD_CAT_TO_PCT = {
    "1": 15.0,  # Baja Humedad (15%)
    "2": 30.0,  # Humedad Media (30%)
    "3": 70.0,  # Alta o saturación (70% o más - elegimos 70 como límite seguro)
}

# --- CAMBIO 4: Mapa de Radiación Solar a MJ/m² (o un valor proxy para ET0) ---
RADIACION_CAT_TO_MJ_M2 = {
    "1": 20.0,  # Soleado (Radiación alta)
    "2": 15.0,  # Parcialmente nublado (Radiación media)
    "3": 10.0,  # Nublado (Radiación baja)
}

# --- CAMBIO 5: Mapa de Velocidad del Viento a m/s (o un valor proxy para ET0) ---
VIENTO_CAT_TO_MS = {
    "1": 0.5,  # Sin viento / Calma
    "2": 2.5,  # Brisa leve
    "3": 5.0,  # Viento fuerte
}