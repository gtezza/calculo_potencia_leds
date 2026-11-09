# Documento de Implementación: Cálculo de Lúmenes, Potencia y Circuitos de LEDs

## 1. Visión General del Proyecto
Este proyecto implementa el sistema de cálculo fotométrico, radiométrico y de conexionado electrónico para LEDs en fototerapia y fotobiomodulación, basándose en la **Clase 5: Cálculos de potencia emitida por los LEDs**.

### Alcance de Módulos:
- **Pasos 1 y 2 (LED Individual):**
  - **Paso 1:** Conversión de Intensidad Luminosa ($I_v$ en mcd o cd) a Flujo Luminoso ($\Phi_v$ en lúmenes) integrando el ángulo sólido $\Omega$.
  - **Paso 2:** Conversión de Flujo Luminoso ($\Phi_v$) a Potencia Radiante Óptica ($\Phi_e$ en mW o Watts) mediante la función de eficacia fotópica $V(\lambda)$ de la CIE ($683 \cdot V(\lambda)$).
  - **Proyección Geométrica y Dosimetría:** Cálculo del radio del haz ($r$), área de la huella ($A$), irradiancia ($E$ en $\text{mW/cm}^2$) y fluencia/dosis ($H$ en $\text{J/cm}^2$).
- **Evolutivo 1 (Conexión Eléctrica y Resistencia Limitadora):**
  - Cálculo de caída de tensión en LEDs y en resistencia limitadora ($V_R = V_{CC} - N \cdot V_F$).
  - Determinación de resistencia teórica y selección automática del valor comercial estándar (Series E12 y E24).
  - Cálculo de potencia disipada ($P_R$) y asignación de potencia comercial mínima recomendada con factor de seguridad ($1/8\text{ W}$, $1/4\text{ W}$, $1/2\text{ W}$, $1\text{ W}$, etc.).
  - Corriente real y eficiencia energética del circuito ($\%$).
- **Evolutivo 2 (Array / Matriz de LEDs para Paneles de Fototerapia):**
  - Acumulación de potencia radiante óptica total ($P_{\text{total}} = N \cdot P_1$) y lúmenes totales ($\Phi_{v,\text{total}} = N \cdot \Phi_{v,1}$).
  - Modelo de matriz de LEDs (filas $\times$ columnas) con espaciado entre centros (pitch).
  - Superposición de conos de luz a distancia $d$: evaluación de solapamiento cuando el diámetro del haz supera el pitch.
  - Irradiancia media del panel sobre el área iluminada efectiva.
  - Aceleración dosimétrica: reducción de tiempo de tratamiento para dosis objetivo terapéuticas (ej: $4\text{ J/cm}^2$).

---

## 2. Arquitectura Modular y Estructura del Repositorio
```
Calculo de radiancia de LEDs/
├── css/
│   └── estilos.css           # Estilos responsivos para Desktop y Tablet con pestañas
├── docs/
│   ├── Clase 5 Calculos de potencia emitida por los LEDs.ppt
│   ├── implementation.md     # Documento técnico de diseño (en español)
│   └── walkthrough.md        # Guía de uso y validación (en español)
├── js/
│   ├── calculos.js           # Motor matemático individual (Pasos 1 y 2)
│   ├── visualizador.js       # Renderizado SVG del cono de emisión
│   ├── resistencia.js        # Motor de cálculo eléctrico E12/E24 y esquemático SVG
│   ├── array.js              # Motor de cálculo de matriz, superposición y visualizador SVG
│   └── interfaz.js           # Controlador general de UI y reactividad
├── py/
│   ├── angulo_solido.py      # Módulo geométrico y ángulo sólido
│   ├── fotometria.py         # Módulo CIE V(λ), tabla de LEDs y conversiones
│   ├── irradiancia_dosis.py  # Módulo de irradiancia y dosis
│   ├── resistencia_limitadora.py # Módulo de cálculo de resistencias E12/E24 y potencias
│   ├── array_leds.py         # Módulo de array de LEDs y superposición
│   ├── perfiles_led.py       # Presets de LEDs de la Clase 5
│   ├── pasos_1_y_2.py        # Orquestador interactivo de consola
│   ├── calculador_lumenes.py # Generador de informes técnicos completos
│   └── pruebas_calculos.py   # Suite de 5 pruebas unitarias automatizadas
└── index.html                # Dashboard web con 3 pestañas interactivas
```

---

## 3. Formulación Matemática de los Evolutivos

### Evolutivo 1: Resistencia Limitadora y Conexión
1. **Caída de tensión en LEDs:**
   $$V_{\text{LEDs}} = N_s \times V_F$$
2. **Caída de tensión en la resistencia:**
   $$V_R = V_{CC} - V_{\text{LEDs}}$$
3. **Resistencia teórica:**
   $$R_{\text{teórica}} = \frac{V_R}{I_F\text{ [A]}} \implies R_{\text{comercial}} \in \text{Serie E12/E24}$$
4. **Potencia disipada real en la resistencia:**
   $$P_{R} = \frac{V_R^2}{R_{\text{comercial}}} \implies P_{\text{comercial}} \ge P_R \times 1.75$$

### Evolutivo 2: Array de LEDs
1. **Potencia Óptica Total:**
   $$P_{\text{óptica total}} = N \times P_{\text{óptica individual}} = (N_{\text{filas}} \times N_{\text{cols}}) \times P_1$$
2. **Flujo Luminoso Total:**
   $$\Phi_{v,\text{total}} = N \times \Phi_{v,1}$$
3. **Área Efectiva a distancia $d$ (expansión $r = d \cdot \tan(\theta_{1/2})$):**
   $$A_{\text{efectiva}} = (L_x + 2r) \times (L_y + 2r)$$
4. **Irradiancia Media del Array:**
   $$E_{\text{array}} = \frac{P_{\text{óptica total}}}{A_{\text{efectiva}}} \quad [\text{mW/cm}^2]$$
5. **Tiempo para Dosis Objetivo ($H$):**
   $$t_{\text{array}}\text{ [s]} = \frac{H\text{ [J/cm}^2] \times 1000}{E_{\text{array}}\text{ [mW/cm}^2]}$$
