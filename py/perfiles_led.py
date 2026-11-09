"""
Definición de perfiles y presets de LEDs comunes extraídos de la Clase 5 y datasheets comerciales.
Permite autocompletar valores típicos o usarlos de referencia para la carga manual.
"""

from typing import Dict, Any

PERFILES_LEDS: Dict[str, Dict[str, Any]] = {
    "rojo_660_clase": {
        "nombre": "LED Rojo Profundo (Ejemplo Clase 5)",
        "intensidad_mcd": 5000.0,
        "angulo_total_grados": 30.0,
        "longitud_onda_nm": 660.0,
        "vf_voltios": 2.0,
        "if_ma": 20.0,
        "distancia_defecto_cm": 2.0,
        "descripcion": "Utilizado para fotobiomodulación y regeneración tisular (Slide 27).",
    },
    "azul_465_clase": {
        "nombre": "LED Azul 14000 mcd (Ejemplo Clase 5)",
        "intensidad_mcd": 14000.0,
        "angulo_total_grados": 30.0,
        "longitud_onda_nm": 465.0,
        "vf_voltios": 3.2,
        "if_ma": 20.0,
        "distancia_defecto_cm": 2.0,
        "descripcion": "Utilizado para acné y tratamientos dermatológicos (Slides 16 y 19).",
    },
    "verde_525": {
        "nombre": "LED Verde Estándar 525 nm",
        "intensidad_mcd": 8000.0,
        "angulo_total_grados": 20.0,
        "longitud_onda_nm": 525.0,
        "vf_voltios": 3.2,
        "if_ma": 20.0,
        "distancia_defecto_cm": 2.0,
        "descripcion": "Alta sensibilidad visual humana (Slide 20).",
    },
    "amarillo_590": {
        "nombre": "LED Amarillo / Ámbar 590 nm",
        "intensidad_mcd": 4000.0,
        "angulo_total_grados": 30.0,
        "longitud_onda_nm": 590.0,
        "vf_voltios": 2.1,
        "if_ma": 20.0,
        "distancia_defecto_cm": 2.0,
        "descripcion": "Utilizado para estimulación linfática y colágeno.",
    },
    "uva_395": {
        "nombre": "LED UV-A Cercano 395 nm",
        "intensidad_mcd": 500.0,
        "angulo_total_grados": 25.0,
        "longitud_onda_nm": 395.0,
        "vf_voltios": 3.4,
        "if_ma": 20.0,
        "distancia_defecto_cm": 2.0,
        "descripcion": "Baja respuesta visual humana, alta energía fotónica.",
    },
}

