# Documento de Implementación: Cálculo de Lúmenes y Potencia Radiante de LEDs

## 1. Visión General del Proyecto
Este proyecto implementa el sistema de cálculo fotométrico y radiométrico para LEDs utilizados en fototerapia y fotobiomodulación, basándose íntegramente en las formulaciones teóricas y experimentales de la **Clase 5: Cálculos de potencia emitida por los LEDs**.

El objetivo primordial es resolver con precisión los **Pasos 1 y 2**:
- **Paso 1:** Conversión de Intensidad Luminosa ($I_v$ en mcd o cd) a Flujo Luminoso ($\Phi_v$ en lúmenes) integrando el ángulo sólido $\Omega$.
- **Paso 2:** Conversión de Flujo Luminoso ($\Phi_v$) a Potencia Radiante Óptica ($\Phi_e$ en mW o Watts) mediante la función de eficacia fotópica $V(\lambda)$ de la CIE ($683 \cdot V(\lambda)$).
- **Proyección Geométrica y Dosimetría:** Cálculo del radio del haz ($r$), área de la huella ($A$), irradiancia ($E$ en $\text{mW/cm}^2$) y fluencia/dosis ($H$ en $\text{J/cm}^2$) en función de la distancia $d$ y el tiempo $t$.

---

## 2. Arquitectura Modular y Estructura del Repositorio
Siguiendo la regla de granularidad funcional y separación de responsabilidades:

```
Calculo de radiancia de LEDs/
├── css/
│   └── estilos.css           # Estilos modernos, responsive para tablet y desktop
├── data/
│   └── (datos de configuración y tablas de referencia)
├── docs/
│   ├── Clase 5 Calculos de potencia emitida por los LEDs.ppt
│   ├── implementation.md     # Documento técnico de diseño (en español)
│   └── walkthrough.md        # Guía de uso y validación (en español)
├── js/
│   ├── calculos.js           # Motor matemático de fotometría y radiometría
│   ├── visualizador.js       # Renderizado interactivo SVG del cono de emisión
│   └── interfaz.js           # Controlador de UI y reactividad en tiempo real
├── py/
│   ├── angulo_solido.py      # Cálculo de semi-ángulo, ángulo sólido y geometría
│   ├── fotometria.py         # Curva CIE V(λ), tabla de LEDs y conversiones
│   ├── irradiancia_dosis.py  # Cálculo de irradiancia y tabla de dosis por tiempos
│   ├── perfiles_led.py       # Presets de LEDs reales de la Clase 5
│   ├── pasos_1_y_2.py        # Orquestador de consola con entrada manual
│   ├── calculador_lumenes.py # Calculador integral y generador de informes
│   └── pruebas_calculos.py   # Suite de pruebas unitarias automatizadas
└── index.html                # Dashboard web local (compatible con Chrome, Firefox, Brave, Edge)
```

---

## 3. Fundamentos Matemáticos y Fórmulas Implementadas

### Paso 1: Milicandelas a Lúmenes
1. **Semi-ángulo del haz ($\theta_{1/2}$):**
   $$\theta_{1/2} = \frac{\theta_{\text{total}}}{2}$$
2. **Ángulo sólido ($\Omega$ en estereorradianes, sr):**
   $$\Omega = 2\pi \cdot (1 - \cos(\theta_{1/2}))$$
3. **Flujo Luminoso ($\Phi_v$ en lúmenes):**
   $$\Phi_v = \left(\frac{I_v\text{ [mcd]}}{1000}\right) \cdot \Omega$$

### Paso 2: Lúmenes a Potencia Radiante Óptica
1. **Factor de Eficacia Fotópica Espectral CIE:**
   $$\text{Eficacia} = 683 \cdot V(\lambda) \quad [\text{lm/W}]$$
2. **Potencia Óptica ($\Phi_e$ o $P_{\text{óptica}}$):**
   $$\Phi_e\text{ [W]} = \frac{\Phi_v}{683 \cdot V(\lambda)} \implies P_{\text{óptica}}\text{ [mW]} = \Phi_e \times 1000$$

### Geometría y Dosimetría a Distancia $d$:
1. **Radio del haz:**
   $$r = d \cdot \tan(\theta_{1/2})$$
2. **Área iluminada:**
   $$A = \pi \cdot r^2 \quad (\text{si } d=0, A \approx 0.15\text{ cm}^2)$$
3. **Irradiancia ($E$):**
   $$E = \frac{P_{\text{óptica}}\text{ [mW]}}{A\text{ [cm}^2]} \quad [\text{mW/cm}^2]$$
4. **Dosis o Fluencia ($H$):**
   $$H = \frac{E \times t\text{ [s]}}{1000} \quad [\text{J/cm}^2]$$

---

## 4. Compatibilidad Multi-Navegador y Responsividad
- **Navegadores validados:** Google Chrome, Mozilla Firefox, Brave y Microsoft Edge.
- **Estándares:** HTML5 semántico, CSS3 con Flexbox, CSS Grid y variables nativas sin dependencias externas bloqueantes.
- **Responsividad:** Adaptable fluidamente hasta formato Tablet (pantallas entre 768px y 1024px) y Desktop (1200px+).

---

## 5. Validación y Pruebas Unitarias
El archivo [`py/pruebas_calculos.py`](file:///c:/Proyectos/Calculo%20de%20radiancia%20de%20LEDs/py/pruebas_calculos.py) verifica con exactitud matemática contra los ejemplos resueltos de la presentación:
- **LED Rojo 660 nm (Diapositiva 27):** 5000 mcd, 30°, 2 cm, 60 s $\implies \Phi_v = 1.07\text{ lm}$, $P = 25.69\text{ mW}$, $E = 28.5\text{ mW/cm}^2$, $H = 1.71\text{ J/cm}^2$.
- **LED Azul 465 nm (Diapositiva 16):** 30°, 2 cm, $P = 16\text{ mW} \implies r = 0.536\text{ cm}$, $A = 0.90\text{ cm}^2$, $E = 17.7\text{ mW/cm}^2$.
