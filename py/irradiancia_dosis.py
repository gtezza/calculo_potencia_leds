"""
Módulo de cálculo de irradiancia y dosis de energía (fluencia) para fototerapia.
Basado en las diapositivas 16, 19, 25, 26 y 27 de la Clase 5.
"""

from typing import Dict, Any


def calcular_irradiancia(potencia_optica_mw: float, area_cm2: float) -> float:
    """
    Calcula la irradiancia media del haz en mW/cm².
    Fórmula: E = P_optica [mW] / A [cm²]
    
    Parámetros:
        potencia_optica_mw (float): Potencia radiante óptica en mW.
        area_cm2 (float): Área de la huella del haz en cm².
        
    Retorna:
        float: Irradiancia en mW/cm².
    """
    if area_cm2 <= 0:
        raise ValueError("El área debe ser mayor a 0 cm².")
    if potencia_optica_mw < 0:
        raise ValueError("La potencia óptica no puede ser negativa.")
    
    return potencia_optica_mw / area_cm2


def calcular_dosis(irradiancia_mw_cm2: float, tiempo_segundos: float) -> float:
    """
    Calcula la dosis de energía o fluencia en Joules por centímetro cuadrado (J/cm²).
    Fórmula: H = (E [mW/cm²] * t [segundos]) / 1000
    
    Parámetros:
        irradiancia_mw_cm2 (float): Irradiancia incidente en mW/cm².
        tiempo_segundos (float): Tiempo de exposición en segundos.
        
    Retorna:
        float: Dosis resultante en J/cm².
    """
    if tiempo_segundos < 0:
        raise ValueError("El tiempo no puede ser negativo.")
    if irradiancia_mw_cm2 < 0:
        raise ValueError("La irradiancia no puede ser negativa.")
    
    return (irradiancia_mw_cm2 * tiempo_segundos) / 1000.0


def tabla_dosis_por_tiempos(irradiancia_mw_cm2: float) -> Dict[str, float]:
    """
    Genera la tabla de dosis de energía para tiempos estándar (1, 5, 10, 15 y 20 minutos),
    tal como figura en la Diapositiva 19.
    """
    tiempos = {
        "1 minuto (60 s)": 60.0,
        "5 minutos (300 s)": 300.0,
        "10 minutos (600 s)": 600.0,
        "15 minutos (900 s)": 900.0,
        "20 minutos (1200 s)": 1200.0,
    }
    return {etiqueta: calcular_dosis(irradiancia_mw_cm2, segs) for etiqueta, segs in tiempos.items()}


if __name__ == "__main__":
    # Prueba del ejemplo resuelto en Diapositiva 27:
    # Potencia: 25.69 mW, Área: 0.9022 cm², Tiempo: 60 s
    irradiancia = calcular_irradiancia(25.69, 0.9022)
    dosis = calcular_dosis(irradiancia, 60.0)
    
    print(f"Irradiancia calculada: {irradiancia:.2f} mW/cm² (Esperado: ~28.5 mW/cm²)")
    print(f"Dosis a 60s: {dosis:.2f} J/cm² (Esperado: ~1.71 J/cm²)")
