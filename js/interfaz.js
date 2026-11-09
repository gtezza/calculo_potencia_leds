/**
 * Controlador de interfaz de usuario y eventos.
 * Vincula la entrada manual, los presets de LEDs y la actualización reactiva en pantalla.
 */

document.addEventListener("DOMContentLoaded", () => {
  const selectPreset = document.getElementById("select-preset");
  const inputMcd = document.getElementById("input-mcd");
  const inputAngulo = document.getElementById("input-angulo");
  const sliderAngulo = document.getElementById("slider-angulo");
  const inputOnda = document.getElementById("input-onda");
  const inputDistancia = document.getElementById("input-distancia");
  const sliderDistancia = document.getElementById("slider-distancia");
  const inputTiempo = document.getElementById("input-tiempo");
  const badgeColor = document.getElementById("badge-color");

  // Llenar el selector de presets
  if (selectPreset) {
    selectPreset.innerHTML = '<option value="personalizado">-- Ingreso Manual / Personalizado --</option>';
    for (const key in TABLA_LEDS_CIE) {
      const led = TABLA_LEDS_CIE[key];
      const opt = document.createElement("option");
      opt.value = key;
      opt.textContent = `${led.nombre} (${led.mcdDefecto} mcd, ${led.anguloDefecto}°)`;
      if (key === "rojo_660") opt.selected = true; // Seleccionado por defecto (Ejemplo clase)
      selectPreset.appendChild(opt);
    }
  }

  // Sincronizar inputs numéricos y sliders
  function sincronizar(inputNum, slider) {
    if (!inputNum || !slider) return;
    inputNum.addEventListener("input", () => {
      slider.value = inputNum.value;
      recalcularTodo();
    });
    slider.addEventListener("input", () => {
      inputNum.value = slider.value;
      recalcularTodo();
    });
  }

  sincronizar(inputAngulo, sliderAngulo);
  sincronizar(inputDistancia, sliderDistancia);

  if (inputMcd) inputMcd.addEventListener("input", recalcularTodo);
  if (inputOnda) inputOnda.addEventListener("input", recalcularTodo);
  if (inputTiempo) inputTiempo.addEventListener("input", recalcularTodo);

  // Al cambiar preset, autocompletar variables dejando opción a modificarlas a mano
  if (selectPreset) {
    selectPreset.addEventListener("change", () => {
      const val = selectPreset.value;
      if (val !== "personalizado" && TABLA_LEDS_CIE[val]) {
        const led = TABLA_LEDS_CIE[val];
        inputMcd.value = led.mcdDefecto;
        inputAngulo.value = led.anguloDefecto;
        if (sliderAngulo) sliderAngulo.value = led.anguloDefecto;
        inputOnda.value = led.longitudOnda;
        inputDistancia.value = led.distanciaDefecto;
        if (sliderDistancia) sliderDistancia.value = led.distanciaDefecto;
      }
      recalcularTodo();
    });
  }

  function recalcularTodo() {
    const mcd = parseFloat(inputMcd.value) || 0;
    const angulo = parseFloat(inputAngulo.value) || 30;
    const onda = parseFloat(inputOnda.value) || 660;
    const distancia = parseFloat(inputDistancia.value) || 0;
    const tiempo = parseFloat(inputTiempo.value) || 60;

    // 1. Paso 1: Milicandelas a Lúmenes
    const p1 = calcularPaso1(mcd, angulo);

    // 2. Paso 2: Lúmenes a Potencia Óptica
    const p2 = calcularPaso2(p1.flujoLumenes, onda);

    // 3. Geometría a la distancia d
    const geo = calcularGeometria(distancia, p1.semiAnguloGrados);

    // 4. Irradiancia y Dosis
    const irrDosis = calcularIrradianciaYDosis(p2.potenciaOpticaMw, geo.areaCm2, tiempo);

    // Determinar color visual según longitud de onda
    let colorHex = "#e63946";
    for (const key in TABLA_LEDS_CIE) {
      if (Math.abs(TABLA_LEDS_CIE[key].longitudOnda - onda) <= 8) {
        colorHex = TABLA_LEDS_CIE[key].colorHex;
        break;
      }
    }
    if (badgeColor) {
      badgeColor.style.backgroundColor = colorHex;
      badgeColor.style.boxShadow = `0 0 12px ${colorHex}`;
    }

    // Actualizar tarjetas de salida en pantalla
    document.getElementById("out-lumenes").textContent = p1.flujoLumenes.toFixed(4) + " lm";
    document.getElementById("out-potencia-mw").textContent = p2.potenciaOpticaMw.toFixed(2) + " mW";
    document.getElementById("out-potencia-w").textContent = p2.potenciaOpticaW.toFixed(6) + " W";
    document.getElementById("out-angulo-solido").textContent = p1.anguloSolidoSr.toFixed(4) + " sr";
    document.getElementById("out-v-lambda").textContent = p2.vLambda.toFixed(6);
    document.getElementById("out-factor-eficacia").textContent = p2.factorEficaciaLmW.toFixed(2) + " lm/W";

    // Actualizar geometría
    document.getElementById("out-radio").textContent = geo.radioCm.toFixed(3) + " cm";
    document.getElementById("out-area").textContent = geo.areaCm2.toFixed(3) + " cm²";
    document.getElementById("out-irradiancia").textContent = irrDosis.irradianciaMwCm2.toFixed(2) + " mW/cm²";
    document.getElementById("out-dosis").textContent = irrDosis.dosisJCm2.toFixed(2) + " J/cm²";

    // Desglose de fórmulas con valores sustituidos en vivo
    document.getElementById("formula-p1").innerHTML = `
      <div class="formula-linea"><b>Semi-ángulo:</b> θ<sub>1/2</sub> = ${p1.anguloTotalGrados}° / 2 = <b>${p1.semiAnguloGrados.toFixed(1)}°</b></div>
      <div class="formula-linea"><b>Ángulo Sólido:</b> Ω = 2π × (1 - cos(${p1.semiAnguloGrados.toFixed(1)}°)) = <b>${p1.anguloSolidoSr.toFixed(4)} sr</b></div>
      <div class="formula-linea"><b>Flujo Luminoso:</b> Φ<sub>v</sub> = (${p1.intensidadMcd} / 1000) × ${p1.anguloSolidoSr.toFixed(4)} sr = <b class="resaltado">${p1.flujoLumenes.toFixed(4)} lm</b></div>
    `;

    document.getElementById("formula-p2").innerHTML = `
      <div class="formula-linea"><b>Eficacia Espectral:</b> 683 × V(${p2.longitudOndaNm} nm) = 683 × ${p2.vLambda.toFixed(6)} = <b>${p2.factorEficaciaLmW.toFixed(2)} lm/W</b></div>
      <div class="formula-linea"><b>Potencia Radiante:</b> Φ<sub>e</sub> = ${p1.flujoLumenes.toFixed(4)} lm / ${p2.factorEficaciaLmW.toFixed(2)} lm/W = <b class="resaltado">${p2.potenciaOpticaMw.toFixed(2)} mW</b></div>
    `;

    document.getElementById("formula-geo").innerHTML = `
      <div class="formula-linea"><b>Radio a ${geo.distanciaCm.toFixed(1)} cm:</b> r = ${geo.distanciaCm.toFixed(1)} × tan(${p1.semiAnguloGrados.toFixed(1)}°) = <b>${geo.radioCm.toFixed(3)} cm</b></div>
      <div class="formula-linea"><b>Área Iluminada:</b> A = π × (${geo.radioCm.toFixed(3)})² = <b>${geo.areaCm2.toFixed(3)} cm²</b></div>
      <div class="formula-linea"><b>Irradiancia Media:</b> E = ${p2.potenciaOpticaMw.toFixed(2)} mW / ${geo.areaCm2.toFixed(3)} cm² = <b>${irrDosis.irradianciaMwCm2.toFixed(2)} mW/cm²</b></div>
      <div class="formula-linea"><b>Dosis a ${tiempo}s:</b> H = (${irrDosis.irradianciaMwCm2.toFixed(2)} × ${tiempo}) / 1000 = <b class="resaltado">${irrDosis.dosisJCm2.toFixed(2)} J/cm²</b></div>
    `;

    // Actualizar tabla de dosificación por tiempos
    const tbodyTiempos = document.getElementById("tbody-tiempos");
    if (tbodyTiempos) {
      tbodyTiempos.innerHTML = irrDosis.tablaDosis.map(fila => `
        <tr>
          <td>${fila.etiqueta}</td>
          <td><b>${fila.dosis.toFixed(2)} J/cm²</b></td>
        </tr>
      `).join("");
    }

    // Actualizar gráfico vectorial SVG
    actualizarVisualizador({
      semiAnguloGrados: p1.semiAnguloGrados,
      distanciaCm: geo.distanciaCm,
      radioCm: geo.radioCm,
      colorHex,
      longitudOndaNm: onda
    });
  }

  // Primera ejecución para inicializar el dashboard
  if (selectPreset && selectPreset.value !== "personalizado") {
    selectPreset.dispatchEvent(new Event("change"));
  } else {
    recalcularTodo();
  }
});
