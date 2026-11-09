"""
Suite de pruebas unitarias y de validación para los cálculos fotométricos, radiométricos
y de conexión con resistencia limitadora para LEDs.
"""

import sys
import os
import unittest

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
from resistencia_limitadora import (
    obtener_resistencia_comercial,
    obtener_potencia_comercial,
    calcular_resistencia_individual,
    calcular_resistencia_serie,
    calcular_arreglo_serie_paralelo,
)
from array_leds import (
    calcular_potencia_total_array,
    calcular_superposicion_matriz,
    comparar_dosis_tiempo,
)


class TestCalculosLED(unittest.TestCase):
    
    def test_diapositiva_27_ejemplo_completo_rojo(self):
        """Validación del ejemplo de la Diapositiva 27."""
        res = ejecutar_flujo_completo(
            intensidad_mcd=5000.0,
            angulo_total_grados=30.0,
            longitud_onda_nm=660.0,
            distancia_cm=2.0,
        )
        p1 = res["paso_1"]
        p2 = res["paso_2"]
        geo = res["geometria"]
        
        self.assertAlmostEqual(p1["angulo_solido_sr"], 0.2141, places=3)
        self.assertAlmostEqual(p1["flujo_lumenes"], 1.0705, places=2)
        self.assertAlmostEqual(p2["potencia_optica_mw"], 25.69, delta=0.2)
        self.assertAlmostEqual(geo["radio_haz_cm"], 0.536, delta=0.01)
        self.assertAlmostEqual(geo["area_haz_cm2"], 0.90, delta=0.02)
        
        irr = calcular_irradiancia(p2["potencia_optica_mw"], geo["area_haz_cm2"])
        self.assertAlmostEqual(irr, 28.5, delta=0.2)
        
        dosis = calcular_dosis(irr, 60.0)
        self.assertAlmostEqual(dosis, 1.71, delta=0.05)

    def test_diapositiva_16_led_azul(self):
        """Validación del ejemplo de la Diapositiva 16."""
        semi_ang = calcular_semi_angulo(30.0)
        radio = calcular_radio_haz(2.0, semi_ang)
        area = calcular_area_haz(radio, 2.0)
        irradiancia = calcular_irradiancia(16.0, area)
        
        self.assertAlmostEqual(radio, 0.536, delta=0.01)
        self.assertAlmostEqual(area, 0.90, delta=0.02)
        self.assertAlmostEqual(irradiancia, 17.7, delta=0.2)

    def test_resistencia_individual_5v_2v_20ma(self):
        """Prueba de cálculo de resistencia limitadora para 5V, Vf=2V, If=20mA."""
        calc = calcular_resistencia_individual(v_fuente=5.0, vf_led=2.0, if_ma=20.0, serie="E12")
        self.assertEqual(calc["r_teorica_ohmios"], 150.0)
        self.assertEqual(calc["r_comercial_ohmios"], 150.0)
        self.assertEqual(calc["p_resistencia_teorica_w"], 0.060)
        self.assertEqual(calc["p_resistencia_comercial_w"], 0.125)
        self.assertEqual(calc["if_real_ma"], 20.0)

    def test_resistencia_serie_12v_3leds_20ma(self):
        """Prueba de cálculo para 3 LEDs en serie a 12V (Vf=2.0V)."""
        calc = calcular_resistencia_serie(v_fuente=12.0, vf_led=2.0, num_leds_serie=3, if_ma=20.0, serie="E12")
        self.assertEqual(calc["r_teorica_ohmios"], 300.0)
        self.assertEqual(calc["r_comercial_ohmios"], 330.0)
        self.assertEqual(calc["p_resistencia_comercial_w"], 0.25)
        self.assertAlmostEqual(calc["if_real_ma"], 18.18, delta=0.05)

    def test_array_leds_potencia_total(self):
        """Prueba de cálculo acumulativo de potencia y lúmenes en un array de 10 LEDs."""
        res_arr = calcular_potencia_total_array(
            potencia_optica_un_led_mw=25.69,
            flujo_lumenes_un_led=1.0705,
            total_leds=10,
        )
        self.assertEqual(res_arr["total_leds"], 10)
        self.assertAlmostEqual(res_arr["potencia_total_array_mw"], 256.9, delta=0.1)
        self.assertAlmostEqual(res_arr["lumenes_totales_array"], 10.705, delta=0.01)


if __name__ == "__main__":
    unittest.main()
