"""
Módulo de cálculo de arrays, paneles y matrices de LEDs para fototerapia.
Modela la potencia radiante total, lúmenes acumulados, superposición de haces,
área efectiva del panel, irradiancia del array y comparación dosimétrica.
"""

from typing import Dict, Any, Tuple
import math
from angulo_solido import calcular_semi_angulo, calcular_radio_haz, calcular_area_haz


def calcular_potencia_total_array(
    potencia_optica_un_led_mw: float,
    flujo_lumenes_un_led: float,
    total_leds: int,
) -> Dict[str, float]:
    """
    Calcula la potencia óptica acumulada y el flujo luminoso total emitido por el array.
    Puesto que la emisión de fotones en el espacio libre es aditiva:
      - P_optica_total = N * P_optica_individual
      - Phi_v_total = N * Phi_v_individual
    """
    if total_leds < 1:
        raise ValueError("El array debe contener al menos 1 LED.")
    if potencia_optica_un_led_mw < 0 or flujo_lumenes_un_led < 0:
        raise ValueError("La potencia y los lúmenes deben ser valores no negativos.")

    potencia_total_mw = potencia_optica_un_led_mw * total_leds
    potencia_total_w = potencia_total_mw / 1000.0
    lumenes_totales = flujo_lumenes_un_led * total_leds

    return {
        "total_leds": total_leds,
        "potencia_un_led_mw": potencia_optica_un_led_mw,
        "potencia_total_array_mw": potencia_total_mw,
        "potencia_total_array_w": potencia_total_w,
        "lumenes_un_led": flujo_lumenes_un_led,
        "lumenes_totales_array": lumenes_totales,
    }


def calcular_irradiancia_array_panel(
    potencia_total_array_mw: float,
    ancho_panel_cm: float,
    alto_panel_cm: float,
    distancia_cm: float,
    semi_angulo_grados: float,
) -> Dict[str, Any]:
    """
    Calcula la irradiancia media incidente de un panel de LEDs a una distancia d.
    
    A la distancia d, cada borde del panel se expande por la divergencia del haz:
      - expansion_cm = d * tan(theta_1/2)
      - ancho_efectivo = ancho_panel + 2 * expansion_cm
      - alto_efectivo = alto_panel + 2 * expansion_cm
      - area_iluminada_cm2 = ancho_efectivo * alto_efectivo
      - Irradiancia media E_array = P_optica_total / area_iluminada
    """
    if ancho_panel_cm <= 0 or alto_panel_cm <= 0:
        raise ValueError("Las dimensiones del panel deben ser mayores a 0 cm.")
    if distancia_cm < 0:
        raise ValueError("La distancia no puede ser negativa.")

    semi_rad = math.radians(semi_angulo_grados)
    expansion_haz_cm = distancia_cm * math.tan(semi_rad)

    ancho_efectivo_cm = ancho_panel_cm + (2.0 * expansion_haz_cm)
    alto_efectivo_cm = alto_panel_cm + (2.0 * expansion_haz_cm)
    area_efectiva_cm2 = ancho_efectivo_cm * alto_efectivo_cm

    irradiancia_media_mw_cm2 = (
        potencia_total_array_mw / area_efectiva_cm2 if area_efectiva_cm2 > 0 else 0.0
    )

    return {
        "potencia_total_array_mw": potencia_total_array_mw,
        "ancho_panel_cm": ancho_panel_cm,
        "alto_panel_cm": alto_panel_cm,
        "area_fisica_panel_cm2": ancho_panel_cm * alto_panel_cm,
        "distancia_cm": distancia_cm,
        "expansion_haz_cm": expansion_haz_cm,
        "ancho_efectivo_cm": ancho_efectivo_cm,
        "alto_efectivo_cm": alto_efectivo_cm,
        "area_efectiva_cm2": area_efectiva_cm2,
        "irradiancia_media_mw_cm2": irradiancia_media_mw_cm2,
    }


def calcular_superposicion_matriz(
    filas: int,
    columnas: int,
    espaciado_pitch_cm: float,
    distancia_cm: float,
    semi_angulo_grados: float,
    potencia_un_led_mw: float,
) -> Dict[str, Any]:
    """
    Modela una matriz de LEDs dispuestos en filas x columnas con separación uniforme (pitch).
    Evalúa la superposición de conos lumínicos a la distancia d:
      - Radio del cono individual: r = d * tan(theta_1/2)
      - Diámetro del cono: D = 2 * r
      - Si D > pitch, los haces se solapan, sumando irradiancia en el centro del tejido.
    """
    total_leds = filas * columnas
    radio_cono_cm = calcular_radio_haz(distancia_cm, semi_angulo_grados)
    diametro_cono_cm = 2.0 * radio_cono_cm

    # Grado de superposición: cociente entre el diámetro del haz y el espaciado entre LEDs
    factor_solapamiento = diametro_cono_cm / espaciado_pitch_cm if espaciado_pitch_cm > 0 else 1.0
    hay_solapamiento = diametro_cono_cm > espaciado_pitch_cm

    # Dimensiones físicas del área activa del array
    ancho_panel_cm = (columnas - 1) * espaciado_pitch_cm if columnas > 1 else espaciado_pitch_cm
    alto_panel_cm = (filas - 1) * espaciado_pitch_cm if filas > 1 else espaciado_pitch_cm

    # Añadir margen de borde equivalente a medio espaciado por lado
    ancho_panel_cm += espaciado_pitch_cm
    alto_panel_cm += espaciado_pitch_cm

    potencia_total_mw = potencia_un_led_mw * total_leds

    datos_panel = calcular_irradiancia_array_panel(
        potencia_total_mw,
        ancho_panel_cm,
        alto_panel_cm,
        distancia_cm,
        semi_angulo_grados,
    )

    return {
        "filas": filas,
        "columnas": columnas,
        "total_leds": total_leds,
        "espaciado_pitch_cm": espaciado_pitch_cm,
        "radio_cono_un_led_cm": radio_cono_cm,
        "diametro_cono_un_led_cm": diametro_cono_cm,
        "hay_solapamiento": hay_solapamiento,
        "factor_solapamiento": factor_solapamiento,
        "datos_panel": datos_panel,
    }


def comparar_dosis_tiempo(
    irradiancia_un_led_mw_cm2: float,
    irradiancia_array_mw_cm2: float,
    dosis_objetivo_j_cm2: float = 4.0,
) -> Dict[str, Any]:
    """
    Compara el tiempo necesario para alcanzar una dosis objetivo (ej: 4 J/cm² habitual en fotobiomodulación)
    utilizando un solo LED frente al panel/array completo.
    Fórmula: t [segundos] = (Dosis [J/cm²] * 1000) / Irradiancia [mW/cm²]
    """
    t_un_led_s = (
        (dosis_objetivo_j_cm2 * 1000.0) / irradiancia_un_led_mw_cm2
        if irradiancia_un_led_mw_cm2 > 0
        else float("inf")
    )
    t_array_s = (
        (dosis_objetivo_j_cm2 * 1000.0) / irradiancia_array_mw_cm2
        if irradiancia_array_mw_cm2 > 0
        else float("inf")
    )

    factor_aceleracion = t_un_led_s / t_array_s if t_array_s > 0 else 1.0

    return {
        "dosis_objetivo_j_cm2": dosis_objetivo_j_cm2,
        "tiempo_un_led_segundos": t_un_led_s,
        "tiempo_un_led_minutos": t_un_led_s / 60.0,
        "tiempo_array_segundos": t_array_s,
        "tiempo_array_minutos": t_array_s / 60.0,
        "factor_aceleracion": factor_aceleracion,
    }


if __name__ == "__main__":
    # Prueba: Panel de 24 LEDs rojos (4 filas x 6 columnas), 25.7 mW por LED, pitch 1.5 cm a 2 cm de distancia
    res_matriz = calcular_superposicion_matriz(
        filas=4,
        columnas=6,
        espaciado_pitch_cm=1.5,
        distancia_cm=2.0,
        semi_angulo_grados=15.0,
        potencia_un_led_mw=25.69,
    )
    p = res_matriz["datos_panel"]
    print("--- PRUEBA ARRAY DE LEDS (4x6 = 24 LEDs) ---")
    print(f"Total LEDs: {res_matriz['total_leds']}")
    print(f"Potencia óptica total: {p['potencia_total_array_mw']:.2f} mW ({p['potencia_total_array_mw']/1000:.3f} W)")
    print(f"Área efectiva a 2 cm: {p['area_efectiva_cm2']:.2f} cm²")
    print(f"Irradiancia media: {p['irradiancia_media_mw_cm2']:.2f} mW/cm²")
    print(f"Superposición de conos: {'SÍ' if res_matriz['hay_solapamiento'] else 'NO'} (Factor: {res_matriz['factor_solapamiento']:.2f})")
