# Guía de Uso y Verificación (Walkthrough)

## 1. Introducción
Esta guía explica cómo ejecutar, probar y utilizar el sistema de cálculo de lúmenes y potencia óptica de LEDs, tanto en su versión por consola (Python) como a través del Dashboard Web interactivo.

---

## 2. Ejecución de los Módulos en Python

### Modo Interactivo de Pasos 1 y 2
Para ejecutar el cálculo interactivo donde puedes ingresar manualmente la intensidad (mcd), el ángulo total de apertura, la longitud de onda y la distancia:

```powershell
python py/pasos_1_y_2.py
```

Al iniciarse, te permitirá:
1. **Cargar variables a mano:** Escribe directamente los valores deseados (por ejemplo: `5000` mcd, `30` grados, `660` nm y `2.0` cm).
2. **Usar presets de la Clase 5:** Selecciona entre los LEDs predefinidos (rojo 660 nm, azul 465 nm, verde 525 nm, etc.) y solo modifica la distancia si lo deseas.

### Ejecución de Pruebas Automatizadas
Para verificar que todas las fórmulas coinciden con los ejercicios de la presentación:

```powershell
python py/pruebas_calculos.py
```
*Salida esperada:*
```
..
----------------------------------------------------------------------
Ran 2 tests in 0.000s

OK
```

---

## 3. Uso del Dashboard Web Interactivo
El dashboard [`index.html`](file:///c:/Proyectos/Calculo%20de%20radiancia%20de%20LEDs/index.html) puede abrirse directamente en cualquiera de los navegadores soportados:
- **Google Chrome**
- **Mozilla Firefox**
- **Brave**
- **Microsoft Edge**

### Cómo abrirlo en tu navegador favorito:
Puedes hacer doble clic en el archivo `index.html` en el explorador de Windows, o ejecutar en PowerShell:

```powershell
# En Microsoft Edge
Start-Process msedge.exe "c:\Proyectos\Calculo de radiancia de LEDs\index.html"

# O en Google Chrome
Start-Process chrome.exe "c:\Proyectos\Calculo de radiancia de LEDs\index.html"

# O en Brave
Start-Process brave.exe "c:\Proyectos\Calculo de radiancia de LEDs\index.html"
```

### Funcionalidades del Dashboard:
1. **Selector de Presets:** Carga automáticamente los parámetros estándar de los LEDs de la Clase 5.
2. **Entrada Manual en Tiempo Real:** Modifica cualquier campo (mcd, ángulo con slider, longitud de onda, distancia con slider y tiempo de exposición).
3. **Métricas en Vivo:** Actualización inmediata de Flujo Luminoso (lúmenes), Potencia Óptica (mW), Irradiancia ($\text{mW/cm}^2$) y Dosis ($\text{J/cm}^2$).
4. **Desglose Matemático Paso a Paso:** Muestra las fórmulas con los números reemplazados en vivo tal como se enseñó en clase.
5. **Gráfico Vectorial SVG Dinámico:** El haz de luz, su ángulo, la distancia $d$ y el radio de la huella $r$ se redibujan en tiempo real con el color exacto de la longitud de onda.
6. **Diseño Responsive:** Totalmente funcional y cómodo en pantallas de escritorio y tablets (768px a 1024px).

---

## 4. Subida y Sincronización con Git
Para versionar los archivos y artefactos en el repositorio remoto configurado (`https://github.com/gtezza/calculo_potencia_leds.git`):

```powershell
git add .
git commit -m "Implementacion modular de Pasos 1 y 2 y Dashboard Web de Calculo de Lumenes y Potencia"
git push origin main
```
