"""
Módulo de cálculo de conexión eléctrica y resistencia limitadora para LEDs.
Permite calcular configuraciones de LED individual, LEDs en serie y arreglos serie-paralelo,
determinando valores teóricos, valores comerciales estándar (Series E12 y E24),
potencia disipada, potencia comercial recomendada con factor de seguridad y eficiencia.
"""

from typing import Dict, Any, List, Tuple
import math

# Valores base de la serie comercial E12 (tolerancia 10%)
VALORES_BASE_E12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]

# Valores base de la serie comercial E24 (tolerancia 5%)
VALORES_BASE_E24 = [
    1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
    3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1
]

# Potencias comerciales estándar en Watts
POTENCIAS_COMERCIALES_W = [0.125, 0.25, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0]


def obtener_resistencia_comercial(valor_ohmios: float, serie: str = "E12") -> float:
    """
    Encuentra el valor comercial estándar más cercano superior (o igual) en la serie elegida (E12 o E24).
    Si valor_ohmios <= 0, retorna 0.0.
    """
    if valor_ohmios <= 0:
        return 0.0

    base_serie = VALORES_BASE_E24 if serie.upper() == "E24" else VALORES_BASE_E12
    
    # Determinar la década (potencia de 10)
    decada = 10 ** math.floor(math.log10(valor_ohmios))
    mantisa = valor_ohmios / decada

    # Buscar el valor estándar inmediatamente superior o igual
    for val in base_serie:
        if val >= round(mantisa, 2):
            return round(val * decada, 2)
            
    # Si superó el último valor de la serie, pasa a la siguiente década
    return round(base_serie[0] * decada * 10, 2)


def obtener_potencia_comercial(potencia_disipada_w: float, factor_seguridad: float = 1.75) -> float:
    """
    Determina la potencia comercial mínima recomendada aplicando un factor de seguridad (por defecto 1.75x).
    """
    potencia_requerida = potencia_disipada_w * factor_seguridad
    for p in POTENCIAS_COMERCIALES_W:
        if p >= potencia_requerida:
            return p
    return POTENCIAS_COMERCIALES_W[-1]


def calcular_resistencia_individual(
    v_fuente: float,
    vf_led: float,
    if_ma: float,
    serie: str = "E12",
) -> Dict[str, Any]:
    """
    Calcula la resistencia limitadora para un único LED.
    Fórmulas:
      - V_R = V_fuente - V_f
      - R_teorica = V_R / I_f
      - P_R = V_R * I_f = I_f^2 * R
    """
    if v_fuente <= vf_led:
        raise ValueError(
            f"La tensión de alimentación ({v_fuente} V) debe ser estrictamente mayor a la caída de tensión del LED ({vf_led} V)."
        )
    if if_ma <= 0:
        raise ValueError("La corriente del LED debe ser mayor a 0 mA.")

    if_amperios = if_ma / 1000.0
    v_resistencia = v_fuente - vf_led
    r_teorica = v_resistencia / if_amperios
    r_comercial = obtener_resistencia_comercial(r_teorica, serie)

    # Potencia teórica y con resistencia comercial
    p_teorica_w = v_resistencia * if_amperios
    p_comercial_w = obtener_potencia_comercial(p_teorica_w)

    # Corriente real resultante con la resistencia comercial estándar
    if_real_ma = (v_resistencia / r_comercial) * 1000.0 if r_comercial > 0 else 0.0
    p_real_w = (v_resistencia ** 2) / r_comercial if r_comercial > 0 else 0.0

    # Eficiencia eléctrica del circuito (Potencia en LED / Potencia total consumida)
    p_total_consumida_w = v_fuente * (if_real_ma / 1000.0)
    p_led_util_w = vf_led * (if_real_ma / 1000.0)
    eficiencia_pct = (p_led_util_w / p_total_consumida_w) * 100.0 if p_total_consumida_w > 0 else 0.0

    return {
        "tipo_conexion": "individual",
        "v_fuente": v_fuente,
        "vf_led": vf_led,
        "if_deseada_ma": if_ma,
        "v_caida_resistencia": v_resistencia,
        "r_teorica_ohmios": r_teorica,
        "r_comercial_ohmios": r_comercial,
        "serie_usada": serie,
        "p_resistencia_teorica_w": p_teorica_w,
        "p_resistencia_comercial_w": p_comercial_w,
        "if_real_ma": if_real_ma,
        "p_resistencia_real_w": p_real_w,
        "p_total_circuito_w": p_total_consumida_w,
        "eficiencia_circuito_pct": eficiencia_pct,
    }


def calcular_resistencia_serie(
    v_fuente: float,
    vf_led: float,
    num_leds_serie: int,
    if_ma: float,
    serie: str = "E12",
) -> Dict[str, Any]:
    """
    Calcula la resistencia limitadora para una rama de N LEDs en serie.
    Fórmulas:
      - V_total_leds = N * V_f
      - V_R = V_fuente - V_total_leds
      - R_teorica = V_R / I_f
    """
    if num_leds_serie < 1:
        raise ValueError("La cantidad de LEDs en serie debe ser al menos 1.")

    v_total_leds = num_leds_serie * vf_led
    if v_fuente <= v_total_leds:
        raise ValueError(
            f"Tensión insuficiente: {num_leds_serie} LEDs en serie requieren {v_total_leds:.2f} V, "
            f"pero la fuente suministra {v_fuente:.2f} V. Reduce los LEDs o aumenta la fuente."
        )
    if if_ma <= 0:
        raise ValueError("La corriente del LED debe ser mayor a 0 mA.")

    if_amperios = if_ma / 1000.0
    v_resistencia = v_fuente - v_total_leds
    r_teorica = v_resistencia / if_amperios
    r_comercial = obtener_resistencia_comercial(r_teorica, serie)

    p_teorica_w = v_resistencia * if_amperios
    p_comercial_w = obtener_potencia_comercial(p_teorica_w)

    if_real_ma = (v_resistencia / r_comercial) * 1000.0 if r_comercial > 0 else 0.0
    p_real_w = (v_resistencia ** 2) / r_comercial if r_comercial > 0 else 0.0

    p_total_consumida_w = v_fuente * (if_real_ma / 1000.0)
    p_leds_util_w = v_total_leds * (if_real_ma / 1000.0)
    eficiencia_pct = (p_leds_util_w / p_total_consumida_w) * 100.0 if p_total_consumida_w > 0 else 0.0

    return {
        "tipo_conexion": "serie",
        "num_leds_serie": num_leds_serie,
        "v_fuente": v_fuente,
        "vf_led": vf_led,
        "v_total_leds": v_total_leds,
        "if_deseada_ma": if_ma,
        "v_caida_resistencia": v_resistencia,
        "r_teorica_ohmios": r_teorica,
        "r_comercial_ohmios": r_comercial,
        "serie_usada": serie,
        "p_resistencia_teorica_w": p_teorica_w,
        "p_resistencia_comercial_w": p_comercial_w,
        "if_real_ma": if_real_ma,
        "p_resistencia_real_w": p_real_w,
        "p_total_circuito_w": p_total_consumida_w,
        "eficiencia_circuito_pct": eficiencia_pct,
    }


def calcular_arreglo_serie_paralelo(
    v_fuente: float,
    vf_led: float,
    num_leds_serie_por_rama: int,
    num_ramas_paralelo: int,
    if_ma_por_led: float,
    serie: str = "E12",
) -> Dict[str, Any]:
    """
    Calcula un arreglo o matriz serie-paralelo (ideal para paneles de fototerapia).
    Cada rama serie lleva su propia resistencia limitadora para evitar desbalance térmico.
    """
    if num_ramas_paralelo < 1:
        raise ValueError("La cantidad de ramas en paralelo debe ser al menos 1.")

    calculo_rama = calcular_resistencia_serie(
        v_fuente, vf_led, num_leds_serie_por_rama, if_ma_por_led, serie
    )

    total_leds = num_leds_serie_por_rama * num_ramas_paralelo
    corriente_total_fuente_ma = calculo_rama["if_real_ma"] * num_ramas_paralelo
    potencia_total_circuito_w = v_fuente * (corriente_total_fuente_ma / 1000.0)
    potencia_total_disipada_resistencias_w = calculo_rama["p_resistencia_real_w"] * num_ramas_paralelo

    return {
        "tipo_conexion": "serie_paralelo",
        "num_leds_serie_por_rama": num_leds_serie_por_rama,
        "num_ramas_paralelo": num_ramas_paralelo,
        "total_leds": total_leds,
        "v_fuente": v_fuente,
        "vf_led": vf_led,
        "if_por_led_ma": calculo_rama["if_real_ma"],
        "corriente_total_fuente_ma": corriente_total_fuente_ma,
        "r_por_rama_teorica_ohmios": calculo_rama["r_teorica_ohmios"],
        "r_por_rama_comercial_ohmios": calculo_rama["r_comercial_ohmios"],
        "p_por_resistencia_comercial_w": calculo_rama["p_resistencia_comercial_w"],
        "p_total_disipada_resistencias_w": potencia_total_disipada_resistencias_w,
        "p_total_circuito_w": potencia_total_circuito_w,
        "eficiencia_circuito_pct": calculo_rama["eficiencia_circuito_pct"],
    }


if __name__ == "__main__":
    # Prueba: Fuente de 12V con 3 LEDs rojos (Vf = 2.0V) a 20 mA
    print("--- PRUEBA 1: LED INDIVIDUAL (Fuente 5V, Vf=2.0V, 20mA) ---")
    ind = calcular_resistencia_individual(v_fuente=5.0, vf_led=2.0, if_ma=20.0)
    print(f"R teórica: {ind['r_teorica_ohmios']:.1f} Ω | R comercial: {ind['r_comercial_ohmios']:.1f} Ω")
    print(f"P disipada: {ind['p_resistencia_teorica_w']:.3f} W -> Potencia comercial recomendada: {ind['p_resistencia_comercial_w']} W")
    print(f"If real: {ind['if_real_ma']:.2f} mA | Eficiencia: {ind['eficiencia_circuito_pct']:.1f}%\n")

    print("--- PRUEBA 2: 3 LEDs EN SERIE (Fuente 12V, Vf=2.0V, 20mA) ---")
    serie_res = calcular_resistencia_serie(v_fuente=12.0, vf_led=2.0, num_leds_serie=3, if_ma=20.0)
    print(f"R teórica: {serie_res['r_teorica_ohmios']:.1f} Ω | R comercial: {serie_res['r_comercial_ohmios']:.1f} Ω")
    print(f"P disipada: {serie_res['p_resistencia_teorica_w']:.3f} W -> Potencia comercial: {serie_res['p_resistencia_comercial_w']} W")
    print(f"Eficiencia circuito: {serie_res['eficiencia_circuito_pct']:.1f}%")

