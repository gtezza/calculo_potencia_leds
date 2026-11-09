"""
Módulo de cálculo de geometría angular y ángulo sólido para LEDs.
Basado en las diapositivas 3, 17, 18 y 23 de la Clase 5 de Fototerapia.
"""

import math


def calcular_semi_angulo(angulo_total_grados: float) -> float:
    """
    Calcula el semi-ángulo de apertura del haz (theta_1/2).
    
    Parámetros:
        angulo_total_grados (float): Ángulo total del haz en grados (ej: 30°).
        
    Retorna:
        float: Semi-ángulo en grados (ej: 15°).
    """
    if angulo_total_grados <= 0 or angulo_total_grados >= 180:
        raise ValueError("El ángulo total debe ser mayor a 0° y menor a 180°.")
    return angulo_total_grados / 2.0


def calcular_angulo_solido(semi_angulo_grados: float) -> float:
    """
    Calcula el ángulo sólido (Omega) subtendido por el cono de luz en estereorradianes (sr).
    Fórmula: Omega = 2 * pi * (1 - cos(theta_1/2))
    
    Parámetros:
        semi_angulo_grados (float): Semi-ángulo del haz en grados.
        
    Retorna:
        float: Ángulo sólido en estereorradianes (sr).
    """
    if semi_angulo_grados <= 0 or semi_angulo_grados >= 90:
        raise ValueError("El semi-ángulo debe estar entre 0° y 90°.")
    
    semi_angulo_rad = math.radians(semi_angulo_grados)
    omega = 2.0 * math.pi * (1.0 - math.cos(semi_angulo_rad))
    return omega


def calcular_radio_haz(distancia_cm: float, semi_angulo_grados: float) -> float:
    """
    Calcula el radio de la huella iluminada a una distancia dada.
    Fórmula: r = d * tan(theta_1/2)
    
    Parámetros:
        distancia_cm (float): Distancia del LED a la superficie en cm.
        semi_angulo_grados (float): Semi-ángulo en grados.
        
    Retorna:
        float: Radio de la huella en cm.
    """
    if distancia_cm < 0:
        raise ValueError("La distancia no puede ser negativa.")
    if distancia_cm == 0:
        return 0.0
    
    semi_angulo_rad = math.radians(semi_angulo_grados)
    return distancia_cm * math.tan(semi_angulo_rad)


def calcular_area_haz(radio_cm: float, distancia_cm: float = 1.0) -> float:
    """
    Calcula el área de la huella circular proyectada en cm².
    Fórmula: A = pi * r^2
    Nota: Si d == 0 (contacto directo), se toma el área típica de la lente del LED (~0.15 cm²).
    
    Parámetros:
        radio_cm (float): Radio de la huella en cm.
        distancia_cm (float): Distancia al tejido en cm.
        
    Retorna:
        float: Área iluminada en cm².
    """
    if distancia_cm == 0:
        return 0.15  # Área promedio de lente de 5mm en contacto directo
    return math.pi * (radio_cm ** 2)


if __name__ == "__main__":
    # Prueba con el ejemplo de la Diapositiva 27: Ángulo 30° (semi-ángulo 15°), distancia 2 cm
    theta_total = 30.0
    theta_half = calcular_semi_angulo(theta_total)
    omega = calcular_angulo_solido(theta_half)
    radio = calcular_radio_haz(2.0, theta_half)
    area = calcular_area_haz(radio, 2.0)
    
    print(f"Ángulo total: {theta_total}° -> Semi-ángulo: {theta_half}°")
    print(f"Ángulo sólido: {omega:.4f} sr (Esperado en clase: ~0.214 sr)")
    print(f"Radio a 2 cm: {radio:.4f} cm (Esperado en clase: ~0.536 cm)")
    print(f"Área a 2 cm: {area:.4f} cm² (Esperado en clase: ~0.90 cm²)")

