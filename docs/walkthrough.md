# Guía de Uso y Verificación (Walkthrough)

## 1. Introducción
Esta guía explica cómo ejecutar, probar y aprovechar el sistema de cálculo fotométrico, radiométrico, de resistencias limitadoras y de arrays de LEDs.

---

## 2. Ejecución en Python

### Módulos Granulares
- **Pasos 1 y 2 interactivos:**
  ```powershell
  python py/pasos_1_y_2.py
  ```
- **Cálculo de Conexión y Resistencia Limitadora (Evolutivo 1):**
  ```powershell
  python py/resistencia_limitadora.py
  ```
- **Cálculo de Array / Matriz de LEDs (Evolutivo 2):**
  ```powershell
  python py/array_leds.py
  ```
- **Ejecución de Pruebas Automatizadas:**
  ```powershell
  python py/pruebas_calculos.py
  ```
  *Salida esperada:*
  ```
  .....
  ----------------------------------------------------------------------
  Ran 5 tests in 0.001s

  OK
  ```

---

## 3. Uso del Dashboard Web Interactivo
Abre [`index.html`](file:///c:/Proyectos/Calculo%20de%20radiancia%20de%20LEDs/index.html) en tu navegador favorito:

```powershell
# En Microsoft Edge
Start-Process msedge.exe "c:\Proyectos\Calculo de radiancia de LEDs\index.html"

# O en Google Chrome
Start-Process chrome.exe "c:\Proyectos\Calculo de radiancia de LEDs\index.html"

# O en Brave
Start-Process brave.exe "c:\Proyectos\Calculo de radiancia de LEDs\index.html"
```

### Funcionalidades por Pestaña:
1. **Pestaña 1: LED Individual (Pasos 1 y 2):**
   - Presets de la clase o entrada manual de $I_v$ (mcd), ángulo ($2\theta$), longitud de onda ($\lambda$), distancia ($d$) y tiempo ($t$).
   - Flujo luminoso ($\Phi_v$), potencia radiante ($\Phi_e$), irradiancia media y dosis.
   - Cono luminoso SVG en tiempo real.
2. **Pestaña 2: Conexión y Resistencia Limitadora (Evolutivo 1):**
   - Configura $V_{CC}$ (ej: 12V), $V_F$ (2.0V), $I_F$ (20 mA) y cantidad de LEDs en serie.
   - Elige entre series comerciales E12 y E24.
   - Obtén el valor comercial exacto, potencia recomendada con factor de seguridad de 1.75x, corriente real y eficiencia.
   - Diagrama esquemático vectorial SVG del circuito.
3. **Pestaña 3: Array / Matriz de LEDs (Evolutivo 2):**
   - Configura matriz de filas $\times$ columnas (ej: $4 \times 6 = 24$ LEDs) y espaciado (pitch).
   - Calcula la potencia óptica acumulada en Watts/mW y lúmenes totales.
   - Evalúa si los conos de luz se solapan a la distancia $d$.
   - Calcula el tiempo de tratamiento acelerado para alcanzar una dosis objetivo (ej: 4 J/cm²).
   - Visualizador de la cuadrícula con halos de radiación interactivos.

---

## 4. Subida y Sincronización con Git
Para enviar las actualizaciones al repositorio remoto (`https://github.com/gtezza/calculo_potencia_leds.git`):

```powershell
git add .
git commit -m "Evolutivos 1 y 2: Calculo de conexion, resistencia limitadora E12/E24 y Array de LEDs con superposicion"
git push origin main
```
