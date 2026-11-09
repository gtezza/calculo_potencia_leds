/**
 * Controlador de interfaz de usuario y eventos general.
 * Vincula:
 * 1. Pasos 1 y 2: Lúmenes y Potencia Óptica individual.
 * 2. Evolutivo 1: Conexión Eléctrica y Resistencia Limitadora (E12 / E24).
 * 3. Evolutivo 2: Cálculo integral de Array / Matriz de LEDs para paneles de fototerapia.
 */

document.addEventListener("DOMContentLoaded", () => {
  // Elementos de entrada individual (Pasos 1 y 2)
  const selectPreset = document.getElementById("select-preset");
  const inputMcd = document.getElementById("input-mcd");
  const inputAngulo = document.getElementById("input-angulo");
  const sliderAngulo = document.getElementById("slider-angulo");
  const inputOnda = document.getElementById("input-onda");
  const inputDistancia = document.getElementById("input-distancia");
  const sliderDistancia = document.getElementById("slider-distancia");
  const inputTiempo = document.getElementById("input-tiempo");
  const badgeColor = document.getElementById("badge-color");

  // Elementos de entrada de Conexión y Resistencia (Evolutivo 1)
  const inputVfuente = document.getElementById("input-vfuente");
  const inputVf = document.getElementById("input-vf");
  const inputIf = document.getElementById("input-if");
  const selectConexion = document.getElementById("select-conexion");
  const selectSerieR = document.getElementById("select-serie-r");
  const inputLedsSerieCircuito = document.getElementById("input-leds-serie-circuito");
  const filaLedsSerieCircuito = document.getElementById("fila-leds-serie-circuito");

  // Elementos de entrada de Array de LEDs (Evolutivo 2)
  const inputFilas = document.getElementById("input-filas");
  const inputColumnas = document.getElementById("input-columnas");
  const inputPitch = document.getElementById("input-pitch");
  const inputDosisObjetivo = document.getElementById("input-dosis-objetivo");

  // Navegación por pestañas
  const tabBtns = document.querySelectorAll(".tab-boton");
  const tabContenidos = document.querySelectorAll(".tab-contenido");

  tabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      tabBtns.forEach(b => b.classList.remove("activo"));
      tabContenidos.forEach(c => c.classList.remove("activo"));
      btn.classList.add("activo");
      const targetId = btn.getAttribute("data-tab");
      const targetContent = document.getElementById(targetId);
      if (targetContent) targetContent.classList.add("activo");
    });
  });

  // Llenar selector de presets
  if (selectPreset) {
    selectPreset.innerHTML = '<option value="personalizado">-- Ingreso Manual / Personalizado --</option>';
    for (const key in TABLA_LEDS_CIE) {
      const led = TABLA_LEDS_CIE[key];
      const opt = document.createElement("option");
      opt.value = key;
      opt.textContent = `${led.nombre} (${led.mcdDefecto} mcd, ${led.anguloDefecto}°)`;
      if (key === "rojo_660") opt.selected = true;
      selectPreset.appendChild(opt);
    }
  }

  // Sincronizar inputs y sliders
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

  // Eventos de inputs generales
  [inputMcd, inputOnda, inputTiempo, inputVfuente, inputVf, inputIf, inputFilas, inputColumnas, inputPitch, inputDosisObjetivo, inputLedsSerieCircuito].forEach(el => {
    if (el) el.addEventListener("input", recalcularTodo);
  });

  if (selectConexion) {
    selectConexion.addEventListener("change", () => {
      if (filaLedsSerieCircuito) {
        filaLedsSerieCircuito.style.display = (selectConexion.value === "individual") ? "none" : "block";
      }
      recalcularTodo();
    });
  }

  if (selectSerieR) selectSerieR.addEventListener("change", recalcularTodo);

  // Al cambiar preset de LED
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
        if (inputVf) inputVf.value = led.vfTipico;
      }
      recalcularTodo();
    });
  }

  function recalcularTodo() {
    // 1. Obtener entradas del LED individual
    const mcd = parseFloat(inputMcd?.value) || 0;
    const angulo = parseFloat(inputAngulo?.value) || 30;
    const onda = parseFloat(inputOnda?.value) || 660;
    const distancia = parseFloat(inputDistancia?.value) || 0;
    const tiempo = parseFloat(inputTiempo?.value) || 60;

    // Pasos 1 y 2
    const p1 = calcularPaso1(mcd, angulo);
    const p2 = calcularPaso2(p1.flujoLumenes, onda);
    const geo = calcularGeometria(distancia, p1.semiAnguloGrados);
    const irrDosis = calcularIrradianciaYDosis(p2.potenciaOpticaMw, geo.areaCm2, tiempo);

    // Color visual según longitud de onda
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

    // Actualizar Salidas LED Individual
    actualizarTexto("out-lumenes", p1.flujoLumenes.toFixed(4) + " lm");
    actualizarTexto("out-potencia-mw", p2.potenciaOpticaMw.toFixed(2) + " mW");
    actualizarTexto("out-potencia-w", p2.potenciaOpticaW.toFixed(6) + " W");
    actualizarTexto("out-irradiancia", irrDosis.irradianciaMwCm2.toFixed(2) + " mW/cm²");
    actualizarTexto("out-dosis", irrDosis.dosisJCm2.toFixed(2) + " J/cm²");

    // Desgloses de fórmulas
    const elFp1 = document.getElementById("formula-p1");
    if (elFp1) {
      elFp1.innerHTML = `
        <div class="formula-linea"><b>Semi-ángulo:</b> θ<sub>1/2</sub> = ${p1.anguloTotalGrados}° / 2 = <b>${p1.semiAnguloGrados.toFixed(1)}°</b></div>
        <div class="formula-linea"><b>Ángulo Sólido:</b> Ω = 2π × (1 - cos(${p1.semiAnguloGrados.toFixed(1)}°)) = <b>${p1.anguloSolidoSr.toFixed(4)} sr</b></div>
        <div class="formula-linea"><b>Flujo Luminoso:</b> Φ<sub>v</sub> = (${p1.intensidadMcd} / 1000) × ${p1.anguloSolidoSr.toFixed(4)} sr = <b class="resaltado">${p1.flujoLumenes.toFixed(4)} lm</b></div>
      `;
    }

    const elFp2 = document.getElementById("formula-p2");
    if (elFp2) {
      elFp2.innerHTML = `
        <div class="formula-linea"><b>Eficacia Espectral:</b> 683 × V(${p2.longitudOndaNm} nm) = 683 × ${p2.vLambda.toFixed(6)} = <b>${p2.factorEficaciaLmW.toFixed(2)} lm/W</b></div>
        <div class="formula-linea"><b>Potencia Radiante:</b> Φ<sub>e</sub> = ${p1.flujoLumenes.toFixed(4)} lm / ${p2.factorEficaciaLmW.toFixed(2)} lm/W = <b class="resaltado">${p2.potenciaOpticaMw.toFixed(2)} mW</b></div>
      `;
    }

    const elFgeo = document.getElementById("formula-geo");
    if (elFgeo) {
      elFgeo.innerHTML = `
        <div class="formula-linea"><b>Radio a ${geo.distanciaCm.toFixed(1)} cm:</b> r = ${geo.distanciaCm.toFixed(1)} × tan(${p1.semiAnguloGrados.toFixed(1)}°) = <b>${geo.radioCm.toFixed(3)} cm</b></div>
        <div class="formula-linea"><b>Área Iluminada:</b> A = π × (${geo.radioCm.toFixed(3)})² = <b>${geo.areaCm2.toFixed(3)} cm²</b></div>
        <div class="formula-linea"><b>Irradiancia Media:</b> E = ${p2.potenciaOpticaMw.toFixed(2)} mW / ${geo.areaCm2.toFixed(3)} cm² = <b>${irrDosis.irradianciaMwCm2.toFixed(2)} mW/cm²</b></div>
        <div class="formula-linea"><b>Dosis a ${tiempo}s:</b> H = (${irrDosis.irradianciaMwCm2.toFixed(2)} × ${tiempo}) / 1000 = <b class="resaltado">${irrDosis.dosisJCm2.toFixed(2)} J/cm²</b></div>
      `;
    }

    const tbodyTiempos = document.getElementById("tbody-tiempos");
    if (tbodyTiempos) {
      tbodyTiempos.innerHTML = irrDosis.tablaDosis.map(fila => `
        <tr><td>${fila.etiqueta}</td><td><b>${fila.dosis.toFixed(2)} J/cm²</b></td></tr>
      `).join("");
    }

    // Gráfico de un LED
    actualizarVisualizador({
      semiAnguloGrados: p1.semiAnguloGrados,
      distanciaCm: geo.distanciaCm,
      radioCm: geo.radioCm,
      colorHex,
      longitudOndaNm: onda
    });

    // ========================================================
    // 2. EVOLUTIVO 1: CONEXIÓN Y RESISTENCIA LIMITADORA
    // ========================================================
    const vFuente = parseFloat(inputVfuente?.value) || 12;
    const vfLed = parseFloat(inputVf?.value) || 2.0;
    const ifMa = parseFloat(inputIf?.value) || 20;
    const tipoConexion = selectConexion?.value || "individual";
    const serieR = selectSerieR?.value || "E12";
    const numLedsSerieCircuito = parseInt(inputLedsSerieCircuito?.value, 10) || 3;

    const resCircuito = calcularCircuitoElectrico({
      vFuente,
      vfLed,
      ifMa,
      tipoConexion,
      numLedsSerie: numLedsSerieCircuito,
      numRamas: 1,
      serie: serieR
    });

    if (!resCircuito.error) {
      actualizarTexto("out-r-teorica", resCircuito.rTeorica.toFixed(1) + " Ω");
      actualizarTexto("out-r-comercial", resCircuito.rComercial.toFixed(1) + " Ω (" + serieR + ")");
      actualizarTexto("out-p-resistencia", resCircuito.pRealW.toFixed(3) + " W");
      actualizarTexto("out-p-comercial-r", resCircuito.pComercialW + " W (seguridad 1.75x)");
      actualizarTexto("out-if-real", resCircuito.ifRealMa.toFixed(2) + " mA");
      actualizarTexto("out-eficiencia-circuito", resCircuito.eficienciaPct.toFixed(1) + "%");

      const elFcirc = document.getElementById("formula-circuito");
      if (elFcirc) {
        elFcirc.innerHTML = `
          <div class="formula-linea"><b>Caída en LEDs:</b> V<sub>LEDs</sub> = ${resCircuito.ledsPorRama} × ${resCircuito.vfLed.toFixed(2)} V = <b>${resCircuito.vTotalLeds.toFixed(2)} V</b></div>
          <div class="formula-linea"><b>Caída en Resistencia:</b> V<sub>R</sub> = ${resCircuito.vFuente} V - ${resCircuito.vTotalLeds.toFixed(2)} V = <b>${resCircuito.vResistencia.toFixed(2)} V</b></div>
          <div class="formula-linea"><b>R Teórica:</b> R = ${resCircuito.vResistencia.toFixed(2)} V / ${(ifMa/1000).toFixed(3)} A = <b>${resCircuito.rTeorica.toFixed(1)} Ω</b> → Comercial: <b class="resaltado">${resCircuito.rComercial} Ω</b></div>
          <div class="formula-linea"><b>Potencia en R:</b> P<sub>R</sub> = (${resCircuito.vResistencia.toFixed(2)} V)² / ${resCircuito.rComercial} Ω = <b>${resCircuito.pRealW.toFixed(3)} W</b> → Usar resistencia de <b class="resaltado">${resCircuito.pComercialW} W</b></div>
        `;
      }
      dibujarEsquematicoCircuito(resCircuito, colorHex);
    } else {
      const elFcirc = document.getElementById("formula-circuito");
      if (elFcirc) elFcirc.innerHTML = `<span style="color: #ef4444;">${resCircuito.error}</span>`;
      dibujarEsquematicoCircuito(resCircuito, colorHex);
    }

    // ========================================================
    // 3. EVOLUTIVO 2: ARRAY / MATRIZ DE LEDS
    // ========================================================
    const filas = parseInt(inputFilas?.value, 10) || 4;
    const columnas = parseInt(inputColumnas?.value, 10) || 6;
    const pitch = parseFloat(inputPitch?.value) || 1.5;
    const dosisObj = parseFloat(inputDosisObjetivo?.value) || 4.0;

    const resArray = calcularArrayLeds({
      potenciaUnLedMw: p2.potenciaOpticaMw,
      flujoLumenesUnLed: p1.flujoLumenes,
      semiAnguloGrados: p1.semiAnguloGrados,
      distanciaCm: geo.distanciaCm,
      filas,
      columnas,
      espaciadoPitchCm: pitch,
      dosisObjetivoJCm2: dosisObj
    });

    actualizarTexto("out-array-total-leds", resArray.totalLeds + " LEDs (" + filas + "×" + columnas + ")");
    actualizarTexto("out-array-potencia-total", resArray.potenciaTotalMw.toFixed(1) + " mW (" + resArray.potenciaTotalW.toFixed(3) + " W)");
    actualizarTexto("out-array-lumenes-totales", resArray.lumenesTotales.toFixed(2) + " lm");
    actualizarTexto("out-array-area-efectiva", resArray.areaEfectivaCm2.toFixed(1) + " cm² (" + resArray.anchoEfectivoCm.toFixed(1) + "×" + resArray.altoEfectivoCm.toFixed(1) + " cm)");
    actualizarTexto("out-array-irradiancia", resArray.irradianciaArrayMwCm2.toFixed(2) + " mW/cm²");
    actualizarTexto("out-array-tiempo-dosis", resArray.tiempoArraySeg < 60 ? resArray.tiempoArraySeg.toFixed(0) + " s" : (resArray.tiempoArraySeg / 60).toFixed(1) + " min");
    actualizarTexto("out-array-aceleracion", resArray.aceleracion.toFixed(1) + "x más rápido que 1 solo LED");

    const elFarray = document.getElementById("formula-array");
    if (elFarray) {
      elFarray.innerHTML = `
        <div class="formula-linea"><b>Potencia Óptica Total:</b> P<sub>total</sub> = ${resArray.totalLeds} LEDs × ${p2.potenciaOpticaMw.toFixed(2)} mW = <b class="resaltado">${resArray.potenciaTotalMw.toFixed(1)} mW (${resArray.potenciaTotalW.toFixed(3)} W)</b></div>
        <div class="formula-linea"><b>Flujo Luminoso Total:</b> Φ<sub>v,total</sub> = ${resArray.totalLeds} × ${p1.flujoLumenes.toFixed(4)} lm = <b>${resArray.lumenesTotales.toFixed(2)} lm</b></div>
        <div class="formula-linea"><b>Área Efectiva a ${geo.distanciaCm} cm:</b> A<sub>efectiva</sub> = ${resArray.anchoEfectivoCm.toFixed(1)} cm × ${resArray.altoEfectivoCm.toFixed(1)} cm = <b>${resArray.areaEfectivaCm2.toFixed(1)} cm²</b></div>
        <div class="formula-linea"><b>Irradiancia Media del Array:</b> E<sub>array</sub> = ${resArray.potenciaTotalMw.toFixed(1)} mW / ${resArray.areaEfectivaCm2.toFixed(1)} cm² = <b class="resaltado">${resArray.irradianciaArrayMwCm2.toFixed(2)} mW/cm²</b></div>
        <div class="formula-linea"><b>Tiempo para ${dosisObj} J/cm²:</b> t<sub>array</sub> = (${dosisObj} × 1000) / ${resArray.irradianciaArrayMwCm2.toFixed(2)} = <b>${resArray.tiempoArraySeg.toFixed(1)} s (${(resArray.tiempoArraySeg/60).toFixed(2)} min)</b></div>
      `;
    }

    dibujarMatrizLedsSVG(resArray, colorHex);
  }

  function actualizarTexto(id, texto) {
    const el = document.getElementById(id);
    if (el) el.textContent = texto;
  }

  // Inicializar
  if (selectPreset && selectPreset.value !== "personalizado") {
    selectPreset.dispatchEvent(new Event("change"));
  } else {
    recalcularTodo();
  }
});
