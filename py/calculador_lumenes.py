"""
Calculador principal de lúmenes y parámetros ópticos de LEDs.
Orquesta los módulos angulo_solido, fotometria e irradiancia_dosis.
"""

from typing import Dict, Any
from angulo_solido import (
    calcular_semi_angulo,
    calcular_angulo_solido,
    calcular_radio_haz,
    calcular_area_haz,
)
from fotometria import (
    convertir_mcd_a_lumenes,
    convertir_lumenes_a_potencia_optica,
    convertir_potencia_optica_a_lumenes,
    obtener_factor_v_lambda,
    KM_CIE,
    TABLA_LEDS_CIE,
)
from irradiancia_dosis import (
    calcular_irradiancia,
    calcular_dosis,
    tabla_dosis_por_tiempos,
)


def calcular_led_completo(
    intensidad_mcd: float,
    angulo_total_grados: float,
    longitud_onda_nm: float,
    distancia_cm: float = 2.0,
    tiempo_segundos: float = 60.0,
) -> Dict[str, Any]:
    """
    Realiza el cálculo integral de un LED paso a paso:
    1. Ángulo sólido y semi-ángulo.
    2. Flujo luminoso en lúmenes.
    3. Potencia radiante óptica en mW.
    4. Radio y área iluminada a la distancia d.
    5. Irradiancia incidente.
    6. Dosis de energía y tabla de tiempos.
    """
    semi_angulo = calcular_semi_angulo(angulo_total_grados)
    omega = calcular_angulo_solido(semi_angulo)
    flujo_lumenes = convertir_mcd_a_lumenes(intensidad_mcd, omega)
    
    # Sensibilidad fotópica
    v_lambda = obtener_factor_v_lambda(longitud_onda_nm)
    factor_eficacia = KM_CIE * v_lambda
    
    if factor_eficacia > 0:
        potencia_optica_w = convertir_lumenes_a_potencia_optica(flujo_lumenes, longitud_onda_nm)
        potencia_optica_mw = potencia_optica_w * 1000.0
    else:
        potencia_optica_w = 0.0
        potencia_optica_mw = 0.0
    
    # Geometría del haz
    radio_cm = calcular_radio_haz(distancia_cm, semi_angulo)
    area_cm2 = calcular_area_haz(radio_cm, distancia_cm)
    
    # Radiación y dosis
    if area_cm2 > 0 and potencia_optica_mw > 0:
        irradiancia = calcular_irradiancia(potencia_optica_mw, area_cm2)
        dosis = calcular_dosis(irradiancia, tiempo_segundos)
        tabla_tiempos = tabla_dosis_por_tiempos(irradiancia)
    else:
        irradiancia = 0.0
        dosis = 0.0
        tabla_tiempos = {}
        
    return {
        "intensidad_mcd": intensidad_mcd,
        "angulo_total_grados": angulo_total_grados,
        "semi_angulo_grados": semi_angulo,
        "angulo_solido_sr": omega,
        "flujo_lumenes": flujo_lumenes,
        "longitud_onda_nm": longitud_onda_nm,
        "v_lambda": v_lambda,
        "factor_eficacia_lm_w": factor_eficacia,
        "potencia_optica_mw": potencia_optica_mw,
        "distancia_cm": distancia_cm,
        "radio_haz_cm": radio_cm,
        "area_haz_cm2": area_cm2,
        "irradiancia_mw_cm2": irradiancia,
        "tiempo_segundos": tiempo_segundos,
        "dosis_j_cm2": dosis,
        "tabla_dosis_tiempos": tabla_tiempos,
    }


def imprimir_informe_led(resultados: Dict[str, Any]) -> None:
    """Muestra en consola el desglose detallado de los cálculos."""
    print("=" * 65)
    print(" INFORME TÉCNICO: CÁLCULO DE LÚMENES Y POTENCIA RADIADA ")
    print("=" * 65)
    print(f"• Intensidad luminosa:        {resultados['intensidad_mcd']:.1f} mcd ({resultados['intensidad_mcd']/1000:.3f} cd)")
    print(f"• Ángulo total del haz (2θ):  {resultados['angulo_total_grados']:.1f}°")
    print(f"• Semi-ángulo (θ_1/2):        {resultados['semi_angulo_grados']:.1f}°")
    print(f"• Ángulo sólido (Ω):          {resultados['angulo_solido_sr']:.4f} sr")
    print("-" * 65)
    print(f" ★ FLUJO LUMINOSO EMITIDO:    {resultados['flujo_lumenes']:.4f} LÚMENES (lm)")
    print("-" * 65)
    print(f"• Longitud de onda (λ):       {resultados['longitud_onda_nm']:.1f} nm")
    print(f"• Sensibilidad fotópica V(λ): {resultados['v_lambda']:.6f}")
    print(f"• Eficacia (683 × V(λ)):      {resultados['factor_eficacia_lm_w']:.2f} lm/W")
    print(f"• Potencia radiante óptica:   {resultados['potencia_optica_mw']:.2f} mW")
    print("-" * 65)
    print(f"• Distancia de tratamiento:   {resultados['distancia_cm']:.2f} cm")
    print(f"• Radio de la huella:         {resultados['radio_haz_cm']:.4f} cm")
    print(f"• Área iluminada (A):         {resultados['area_haz_cm2']:.4f} cm²")
    print(f"• Irradiancia media (E):      {resultados['irradiancia_mw_cm2']:.2f} mW/cm²")
    print(f"• Dosis calculada a {resultados['tiempo_segundos']:.0f}s:      {resultados['dosis_j_cm2']:.2f} J/cm²")
    print("=" * 65)
    if resultados["tabla_dosis_tiempos"]:
        print(" Tabla de dosificación estimada:")
        for lapso, j_cm2 in resultados["tabla_dosis_tiempos"].items():
            print(f"   - {lapso:20s}: {j_cm2:.2f} J/cm²")
        print("=" * 65)


if __name__ == "__main__":
    # Ejecución de demostración con los datos de la Diapositiva 27
    res = calcular_led_completo(
        intensidad_mcd=5000.0,
        angulo_total_grados=30.0,
        longitud_onda_nm=660.0,
        distancia_cm=2.0,
        tiempo_segundos=60.0,
    )
    imprimir_informe_led(res)
