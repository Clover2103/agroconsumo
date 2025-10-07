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
STAGE_MAP = {"1": "Siembra", "2": "Crecimiento", "3": "Cosecha"}
SOIL_MAP = {"1": "Arenoso", "2": "Arcilloso", "3": "Franco"}

# Coeficiente de cultivo (Kc)
KC_TABLE = {
    "Maíz": {"Siembra": 0.4, "Crecimiento": 0.9, "Cosecha": 0.6},
    "Arroz": {"Siembra": 1.1, "Crecimiento": 1.2, "Cosecha": 0.9},
    "Café": {"Siembra": 0.5, "Crecimiento": 0.8, "Cosecha": 0.7},
}

# Eficiencias por método de riego
METHOD_EFF = {
    "Goteo": 0.90,
    "Aspersión": 0.75,
    "Surcos": 0.60,
    "Inundación": 0.50,
    "Pivot central": 0.65,
}

# Mapas heurísticos
PRECIP_CAT_TO_MM = {"1": 5.0, "2": 20.0, "3": 50.0}
AGUA_CAT_TO_M3 = {"1": 1000.0, "2": 5000.0, "3": 10000.0}
