"""
Ejecutor modular de los Pasos 1 y 2 para cálculo de Lúmenes y Potencia Óptica de LEDs.
Permite ingresar manualmente las variables del LED y la distancia, o cargar presets.
Basado en las Diapositivas 3, 13, 20, 23 y 24 de la Clase 5.
"""

from typing import Dict, Any, Optional
from angulo_solido import calcular_semi_angulo, calcular_angulo_solido, calcular_radio_haz, calcular_area_haz
from fotometria import (
    convertir_mcd_a_lumenes,
    convertir_lumenes_a_potencia_optica,
    obtener_factor_v_lambda,
    KM_CIE,
)
from perfiles_led import PERFILES_LEDS


def calcular_paso_1(intensidad_mcd: float, angulo_total_grados: float) -> Dict[str, float]:
    """
    PASO 1: Conversión de Milicandelas (mcd) a Flujo Luminoso (Lúmenes)
    
    Ecuaciones:
      - theta_1/2 = angulo_total / 2
      - Omega = 2 * pi * (1 - cos(theta_1/2))
      - Phi_v = (intensidad_mcd / 1000) * Omega
    """
    semi_angulo = calcular_semi_angulo(angulo_total_grados)
    omega = calcular_angulo_solido(semi_angulo)
    flujo_lumenes = convertir_mcd_a_lumenes(intensidad_mcd, omega)
    
    return {
        "intensidad_mcd": intensidad_mcd,
        "intensidad_cd": intensidad_mcd / 1000.0,
        "angulo_total_grados": angulo_total_grados,
        "semi_angulo_grados": semi_angulo,
        "angulo_solido_sr": omega,
        "flujo_lumenes": flujo_lumenes,
    }


def calcular_paso_2(flujo_lumenes: float, longitud_onda_nm: float) -> Dict[str, float]:
    """
    PASO 2: Conversión de Flujo Luminoso (Lúmenes) a Potencia Radiante Óptica (mW / W)
    
    Ecuaciones:
      - V(lambda) = Eficiencia fotópica CIE
      - Factor Eficacia = 683 * V(lambda) [lm/W]
      - Phi_e [W] = Phi_v / (683 * V(lambda))
      - P_optica [mW] = Phi_e * 1000
    """
    v_lambda = obtener_factor_v_lambda(longitud_onda_nm)
    factor_eficacia = KM_CIE * v_lambda
    
    if factor_eficacia > 0:
        potencia_w = convertir_lumenes_a_potencia_optica(flujo_lumenes, longitud_onda_nm)
        potencia_mw = potencia_w * 1000.0
    else:
        potencia_w = 0.0
        potencia_mw = 0.0
        
    return {
        "flujo_lumenes": flujo_lumenes,
        "longitud_onda_nm": longitud_onda_nm,
        "v_lambda": v_lambda,
        "factor_eficacia_lm_w": factor_eficacia,
        "potencia_optica_w": potencia_w,
        "potencia_optica_mw": potencia_mw,
    }


def calcular_geometria_distancia(distancia_cm: float, semi_angulo_grados: float) -> Dict[str, float]:
    """
    Cálculo geométrico del haz en función de la distancia d cargada a mano.
    Ecuaciones:
      - r = d * tan(theta_1/2)
      - A = pi * r^2
    """
    radio_cm = calcular_radio_haz(distancia_cm, semi_angulo_grados)
    area_cm2 = calcular_area_haz(radio_cm, distancia_cm)
    return {
        "distancia_cm": distancia_cm,
        "radio_haz_cm": radio_cm,
        "area_haz_cm2": area_cm2,
    }


def ejecutar_flujo_completo(
    intensidad_mcd: float,
    angulo_total_grados: float,
    longitud_onda_nm: float,
    distancia_cm: float = 2.0,
) -> Dict[str, Any]:
    """Ejecuta los Pasos 1 y 2 más el cálculo geométrico de distancia."""
    p1 = calcular_paso_1(intensidad_mcd, angulo_total_grados)
    p2 = calcular_paso_2(p1["flujo_lumenes"], longitud_onda_nm)
    geo = calcular_geometria_distancia(distancia_cm, p1["semi_angulo_grados"])
    
    return {
        "paso_1": p1,
        "paso_2": p2,
        "geometria": geo,
    }


def mostrar_resultado_consola(res: Dict[str, Any]) -> None:
    """Muestra el resultado con formato claro y pedagógico."""
    p1 = res["paso_1"]
    p2 = res["paso_2"]
    geo = res["geometria"]
    
    print("\n" + "=" * 60)
    print(" PASO 1: CONVERSIÓN DE MILICANDELAS A LÚMENES")
    print("=" * 60)
    print(f"• Intensidad Luminosa (Iv):      {p1['intensidad_mcd']:.1f} mcd ({p1['intensidad_cd']:.3f} cd)")
    print(f"• Ángulo de Apertura Total (2θ): {p1['angulo_total_grados']:.1f}°")
    print(f"• Semi-ángulo de Apertura (θ):   {p1['semi_angulo_grados']:.1f}°")
    print(f"• Ángulo Sólido (Ω):             {p1['angulo_solido_sr']:.4f} estereorradianes (sr)")
    print(f"  Fórmula: Ω = 2π × (1 - cos({p1['semi_angulo_grados']}°))")
    print("-" * 60)
    print(f" ★ FLUJO LUMINOSO CALCULADO:     {p1['flujo_lumenes']:.4f} LÚMENES (lm)")
    print(f"  Fórmula: Φv = ({p1['intensidad_mcd']} / 1000) × {p1['angulo_solido_sr']:.4f}")
    
    print("\n" + "=" * 60)
    print(" PASO 2: CONVERSIÓN DE LÚMENES A POTENCIA ÓPTICA (mW)")
    print("=" * 60)
    print(f"• Longitud de Onda (λ):          {p2['longitud_onda_nm']:.1f} nm")
    print(f"• Eficiencia Fotópica CIE V(λ):  {p2['v_lambda']:.6f}")
    print(f"• Factor de Conversión (683×V):  {p2['factor_eficacia_lm_w']:.2f} lm/W")
    print(f"• Potencia Radiante Óptica:      {p2['potencia_optica_mw']:.2f} mW ({p2['potencia_optica_w']:.6f} W)")
    print(f"  Fórmula: Φe = {p1['flujo_lumenes']:.4f} lm / {p2['factor_eficacia_lm_w']:.2f} lm/W")
    
    print("\n" + "=" * 60)
    print(" PARÁMETROS GEOMÉTRICOS A LA DISTANCIA ESPECIFICADA")
    print("=" * 60)
    print(f"• Distancia al LED (d):          {geo['distancia_cm']:.2f} cm")
    print(f"• Radio del haz proyectado (r):  {geo['radio_haz_cm']:.4f} cm")
    print(f"• Área iluminada (A):            {geo['area_haz_cm2']:.4f} cm²")
    print("=" * 60 + "\n")


def menu_interactivo() -> None:
    """Permite al usuario interactuar desde consola cargando datos a mano o usando presets."""
    print("=============================================================")
    print("   SISTEMA DE CÁLCULO DE LÚMENES Y POTENCIA ÓPTICA DE LEDS   ")
    print("=============================================================")
    print("1. Cargar variables a mano (Intensidad, Ángulo, Longitud de onda, Distancia)")
    print("2. Seleccionar un LED predefinido de la Clase 5")
    opcion = input("Seleccione una opción (1 o 2, Enter=1): ").strip()
    
    if opcion == "2":
        print("\nPresets disponibles:")
        claves = list(PERFILES_LEDS.keys())
        for idx, k in enumerate(claves, 1):
            p = PERFILES_LEDS[k]
            print(f"  {idx}. {p['nombre']} - {p['intensidad_mcd']} mcd, {p['angulo_total_grados']}°, {p['longitud_onda_nm']} nm")
        
        sel = input("Elija el número de preset (Enter=1): ").strip()
        idx_sel = int(sel) - 1 if sel.isdigit() and 1 <= int(sel) <= len(claves) else 0
        preset = PERFILES_LEDS[claves[idx_sel]]
        
        mcd = preset["intensidad_mcd"]
        ang = preset["angulo_total_grados"]
        onda = preset["longitud_onda_nm"]
        dist_sugerida = preset["distancia_defecto_cm"]
        dist_str = input(f"Distancia d en cm [por defecto {dist_sugerida} cm]: ").strip()
        dist = float(dist_str) if dist_str else dist_sugerida
    else:
        print("\n--- INGRESO MANUAL DE VARIABLES DEL LED ---")
        mcd = float(input("• Intensidad luminosa (mcd) [ej: 5000]: ") or "5000")
        ang = float(input("• Ángulo total del haz (grados) [ej: 30]: ") or "30")
        onda = float(input("• Longitud de onda (nm) [ej: 660 para rojo, 465 para azul]: ") or "660")
        dist = float(input("• Distancia a la superficie (cm) [ej: 2.0]: ") or "2.0")
        
    resultado = ejecutar_flujo_completo(mcd, ang, onda, dist)
    mostrar_resultado_consola(resultado)


if __name__ == "__main__":
    menu_interactivo()
