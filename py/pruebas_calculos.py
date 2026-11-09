"""
Suite de pruebas unitarias y de validación para los cálculos fotométricos y radiométricos de LEDs.
Compara los resultados contra los ejemplos resueltos en las Diapositivas 16, 19 y 27 de la Clase 5.
"""

import sys
import os
import unittest

# Asegurar que el directorio py esté en el path de importación
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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
)
from irradiancia_dosis import (
    calcular_irradiancia,
    calcular_dosis,
)
from pasos_1_y_2 import ejecutar_flujo_completo


class TestCalculosLED(unittest.TestCase):
    
    def test_diapositiva_27_ejemplo_completo_rojo(self):
        """
        Validación del ejemplo de la Diapositiva 27:
        LED rojo 660 nm, 5000 mcd, ángulo 30°, distancia 2 cm, tiempo 60 s.
        """
        res = ejecutar_flujo_completo(
            intensidad_mcd=5000.0,
            angulo_total_grados=30.0,
            longitud_onda_nm=660.0,
            distancia_cm=2.0,
        )
        p1 = res["paso_1"]
        p2 = res["paso_2"]
        geo = res["geometria"]
        
        # 1. Ángulo sólido esperado: ~0.214 sr
        self.assertAlmostEqual(p1["angulo_solido_sr"], 0.2141, places=3)
        
        # 2. Flujo luminoso esperado: ~1.07 lm
        self.assertAlmostEqual(p1["flujo_lumenes"], 1.0705, places=2)
        
        # 3. Potencia óptica esperada: ~25.7 mW
        self.assertAlmostEqual(p2["potencia_optica_mw"], 25.69, delta=0.2)
        
        # 4. Radio del haz a 2 cm esperado: ~0.536 cm
        self.assertAlmostEqual(geo["radio_haz_cm"], 0.536, delta=0.01)
        
        # 5. Área del haz esperada: ~0.90 cm²
        self.assertAlmostEqual(geo["area_haz_cm2"], 0.90, delta=0.02)
        
        # 6. Irradiancia esperada: ~28.5 mW/cm²
        irr = calcular_irradiancia(p2["potencia_optica_mw"], geo["area_haz_cm2"])
        self.assertAlmostEqual(irr, 28.5, delta=0.2)
        
        # 7. Dosis esperada a 60s: ~1.71 J/cm²
        dosis = calcular_dosis(irr, 60.0)
        self.assertAlmostEqual(dosis, 1.71, delta=0.05)

    def test_diapositiva_16_led_azul(self):
        """
        Validación del ejemplo de la Diapositiva 16:
        LED azul 30° apertura, distancia 2 cm, potencia 16 mW.
        Radio: 0.536 cm, Área: 0.90 cm², Irradiancia: ~17.7 mW/cm².
        """
        semi_ang = calcular_semi_angulo(30.0)
        radio = calcular_radio_haz(2.0, semi_ang)
        area = calcular_area_haz(radio, 2.0)
        irradiancia = calcular_irradiancia(16.0, area)
        
        self.assertAlmostEqual(radio, 0.536, delta=0.01)
        self.assertAlmostEqual(area, 0.90, delta=0.02)
        self.assertAlmostEqual(irradiancia, 17.7, delta=0.2)


if __name__ == "__main__":
    unittest.main()
