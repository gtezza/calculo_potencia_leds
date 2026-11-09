"""
Módulo de fotometría y radiometría para cálculo de flujo luminoso (lúmenes) y potencia óptica.
Basado en las diapositivas 4, 13, 14, 15, 20 y 24 de la Clase 5 de Fototerapia.
"""

from typing import Dict, Any, Optional

# Constante de eficacia luminosa espectral máxima de la CIE (a 555 nm)
KM_CIE = 683.0  # lm/W

# Tabla de datos espectrales y de eficiencia fotópica extraída de la Clase 5
TABLA_LEDS_CIE: Dict[str, Dict[str, Any]] = {
    "verde_pico": {
        "nombre": "Verde (Pico de máxima visión CIE)",
        "longitud_onda_nm": 555,
        "v_lambda": 1.0000,
        "factor_lm_w": 683.0,
        "vf_tipico": 3.2,
        "wpe_promedio": 0.08,
    },
    "verde_estandar": {
        "nombre": "Verde estándar",
        "longitud_onda_nm": 525,
        "v_lambda": 0.7930,
        "factor_lm_w": 541.6,
        "vf_tipico": 3.2,
        "wpe_promedio": 0.085,
    },
    "amarillo": {
        "nombre": "Amarillo / Ámbar",
        "longitud_onda_nm": 590,
        "v_lambda": 0.7570,
        "factor_lm_w": 517.0,
        "vf_tipico": 2.1,
        "wpe_promedio": 0.115,
    },
    "rojo_estandar": {
        "nombre": "Rojo estándar",
        "longitud_onda_nm": 625,
        "v_lambda": 0.3210,
        "factor_lm_w": 219.2,
        "vf_tipico": 2.0,
        "wpe_promedio": 0.185,
    },
    "rojo_profundo": {
        "nombre": "Rojo profundo / Fotobiomodulación",
        "longitud_onda_nm": 660,
        "v_lambda": 0.0610,
        "factor_lm_w": 41.6,
        "vf_tipico": 2.0,
        "wpe_promedio": 0.20,
    },
    "azul": {
        "nombre": "Azul espectral",
        "longitud_onda_nm": 465,
        "v_lambda": 0.0739,
        "factor_lm_w": 50.5,
        "vf_tipico": 3.15,
        "wpe_promedio": 0.225,
    },
    "uva_cercano": {
        "nombre": "UV-A cercano",
        "longitud_onda_nm": 395,
        "v_lambda": 0.0002,
        "factor_lm_w": 0.13,
        "vf_tipico": 3.35,
        "wpe_promedio": 0.13,
    },
    "uva_estandar": {
        "nombre": "UV-A estándar",
        "longitud_onda_nm": 365,
        "v_lambda": 0.000011,
        "factor_lm_w": 0.0075,
        "vf_tipico": 3.6,
        "wpe_promedio": 0.055,
    },
    "infrarrojo": {
        "nombre": "Infrarrojo cercano (IR)",
        "longitud_onda_nm": 850,
        "v_lambda": 0.0,
        "factor_lm_w": 0.0,  # En IR no aplican lúmenes visuales, se mide directamente en mW
        "vf_tipico": 1.35,
        "wpe_promedio": 0.25,
    },
}


def obtener_factor_v_lambda(longitud_onda_nm: float) -> float:
    """
    Obtiene el factor V(lambda) de sensibilidad fotópica CIE.
    Si coincide con un valor de referencia lo toma de la tabla,
    o aproxima según la curva CIE.
    """
    for datos in TABLA_LEDS_CIE.values():
        if abs(datos["longitud_onda_nm"] - longitud_onda_nm) <= 2:
            return datos["v_lambda"]
    
    # Si está fuera del espectro visible estándar (380 - 750 nm)
    if longitud_onda_nm < 380 or longitud_onda_nm > 750:
        return 0.0
    
    # Aproximación gaussiana estándar de la curva fotópica CIE 1931 centrada en 555 nm
    import math
    return math.exp(-0.5 * ((longitud_onda_nm - 555.0) / 45.0) ** 2)


def convertir_candelas_a_lumenes(intensidad_cd: float, angulo_solido_sr: float) -> float:
    """
    Calcula el flujo luminoso (lúmenes) a partir de la intensidad en candelas y el ángulo sólido.
    Fórmula: Phi_v = I_v * Omega
    """
    if intensidad_cd < 0:
        raise ValueError("La intensidad no puede ser negativa.")
    if angulo_solido_sr < 0:
        raise ValueError("El ángulo sólido no puede ser negativo.")
    return intensidad_cd * angulo_solido_sr


def convertir_mcd_a_lumenes(intensidad_mcd: float, angulo_solido_sr: float) -> float:
    """
    Calcula el flujo luminoso (lúmenes) a partir de milicandelas (mcd).
    Fórmula: Phi_v = (I_v [mcd] / 1000) * Omega
    """
    intensidad_cd = intensidad_mcd / 1000.0
    return convertir_candelas_a_lumenes(intensidad_cd, angulo_solido_sr)


def convertir_lumenes_a_potencia_optica(flujo_lumenes: float, longitud_onda_nm: float) -> float:
    """
    Convierte flujo luminoso (lúmenes) a potencia radiante óptica en Watts (Phi_e).
    Fórmula: Phi_e = Phi_v / (683 * V(lambda))
    """
    v_lambda = obtener_factor_v_lambda(longitud_onda_nm)
    factor = KM_CIE * v_lambda
    if factor <= 0:
        raise ValueError(f"Para longitud de onda {longitud_onda_nm} nm no hay sensibilidad fotópica (V(lambda) = 0). "
                         f"Debe utilizarse directamente la potencia radiante en mW.")
    return flujo_lumenes / factor


def convertir_potencia_optica_a_lumenes(potencia_optica_watts: float, longitud_onda_nm: float) -> float:
    """
    Convierte potencia radiante óptica en Watts a flujo luminoso en lúmenes.
    Fórmula: Phi_v = 683 * V(lambda) * Phi_e
    """
    v_lambda = obtener_factor_v_lambda(longitud_onda_nm)
    factor = KM_CIE * v_lambda
    return factor * potencia_optica_watts


def estimar_potencia_electrica(vf_voltios: float, if_ma: float) -> float:
    """
    Calcula la potencia eléctrica consumida en mW.
    P_electrica = Vf * If
    """
    return vf_voltios * if_ma


def estimar_potencia_optica_por_wpe(potencia_electrica_mw: float, wpe_decimal: float) -> float:
    """
    Estima la potencia radiante óptica en mW mediante la eficiencia radiativa (WPE).
    P_optica = P_electrica * WPE
    """
    return potencia_electrica_mw * wpe_decimal


if __name__ == "__main__":
    # Prueba del ejemplo resuelto en Diapositiva 27:
    # LED 5000 mcd, rojo 660 nm, Omega = 0.2141 sr
    from angulo_solido import calcular_semi_angulo, calcular_angulo_solido
    
    omega_test = calcular_angulo_solido(calcular_semi_angulo(30.0))
    lumenes = convertir_mcd_a_lumenes(5000.0, omega_test)
    potencia_w = convertir_lumenes_a_potencia_optica(lumenes, 660.0)
    potencia_mw = potencia_w * 1000.0
    
    print(f"Flujo luminoso calculado: {lumenes:.4f} lm (Esperado: ~1.07 lm)")
    print(f"Potencia óptica calculada: {potencia_mw:.2f} mW (Esperado: ~25.7 mW)")
