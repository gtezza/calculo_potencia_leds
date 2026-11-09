/**
 * Módulo de cálculo de conexión eléctrica y resistencia limitadora para LEDs.
 * Series comerciales E12 / E24, disipación de potencia, corriente real y esquemático SVG.
 */

const VALORES_E12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2];
const VALORES_E24 = [
  1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
  3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1
];
const POTENCIAS_ESTANDAR = [0.125, 0.25, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0];

function obtenerResistenciaComercialJS(ohmios, serie = "E12") {
  if (ohmios <= 0) return 0;
  const lista = serie === "E24" ? VALORES_E24 : VALORES_E12;
  const decada = Math.pow(10, Math.floor(Math.log10(ohmios)));
  const mantisa = ohmios / decada;

  for (let val of lista) {
    if (val >= Number(mantisa.toFixed(2))) {
      return Number((val * decada).toFixed(2));
    }
  }
  return Number((lista[0] * decada * 10).toFixed(2));
}

function obtenerPotenciaComercialJS(potenciaW, factorSeguridad = 1.75) {
  const req = potenciaW * factorSeguridad;
  for (let p of POTENCIAS_ESTANDAR) {
    if (p >= req) return p;
  }
  return POTENCIAS_ESTANDAR[POTENCIAS_ESTANDAR.length - 1];
}

function calcularCircuitoElectrico(config) {
  const { vFuente, vfLed, ifMa, tipoConexion, numLedsSerie, numRamas, serie } = config;

  if (vFuente <= 0 || vfLed <= 0 || ifMa <= 0) {
    return { error: "Los valores de tensión y corriente deben ser positivos." };
  }

  const ifAmperios = ifMa / 1000.0;
  let vTotalLeds = vfLed;
  let ledsPorRama = 1;
  let totalLeds = 1;
  let ramas = 1;

  if (tipoConexion === "serie") {
    ledsPorRama = numLedsSerie || 1;
    vTotalLeds = ledsPorRama * vfLed;
    totalLeds = ledsPorRama;
  } else if (tipoConexion === "serie_paralelo") {
    ledsPorRama = numLedsSerie || 1;
    ramas = numRamas || 1;
    vTotalLeds = ledsPorRama * vfLed;
    totalLeds = ledsPorRama * ramas;
  }

  if (vFuente <= vTotalLeds) {
    return {
      error: `Tensión insuficiente: ${ledsPorRama} LED(s) requieren ${vTotalLeds.toFixed(2)} V, pero la fuente entrega ${vFuente.toFixed(2)} V. Reduce la cantidad de LEDs o aumenta la fuente.`
    };
  }

  const vResistencia = vFuente - vTotalLeds;
  const rTeorica = vResistencia / ifAmperios;
  const rComercial = obtenerResistenciaComercialJS(rTeorica, serie);

  const pTeoricaW = vResistencia * ifAmperios;
  const pComercialW = obtenerPotenciaComercialJS(pTeoricaW);

  const ifRealMa = rComercial > 0 ? (vResistencia / rComercial) * 1000.0 : 0;
  const pRealW = rComercial > 0 ? Math.pow(vResistencia, 2) / rComercial : 0;

  const corrienteTotalFuenteMa = ifRealMa * ramas;
  const potenciaTotalConsumidaW = vFuente * (corrienteTotalFuenteMa / 1000.0);
  const potenciaLedsUtilW = (vTotalLeds * (ifRealMa / 1000.0)) * ramas;
  const eficienciaPct = potenciaTotalConsumidaW > 0 ? (potenciaLedsUtilW / potenciaTotalConsumidaW) * 100.0 : 0;

  return {
    tipoConexion,
    vFuente,
    vfLed,
    ledsPorRama,
    ramas,
    totalLeds,
    vTotalLeds,
    vResistencia,
    rTeorica,
    rComercial,
    serie,
    pTeoricaW,
    pComercialW,
    ifRealMa,
    pRealW,
    corrienteTotalFuenteMa,
    potenciaTotalConsumidaW,
    potenciaLedsUtilW,
    eficienciaPct
  };
}

/**
 * Genera el diagrama esquemático del circuito en SVG.
 */
function dibujarEsquematicoCircuito(res, colorHex = "#e63946") {
  const contenedor = document.getElementById("contenedor-svg-circuito");
  if (!contenedor) return;

  if (res.error) {
    contenedor.innerHTML = `<div style="color: #ef4444; padding: 20px; text-align: center;"><b>⚠️ Error en el circuito:</b><br>${res.error}</div>`;
    return;
  }

  const ancho = 540;
  const alto = 220;
  const xFuente = 60;
  const xRes = 180;
  const xLedInicio = 290;
  const ySuperior = 60;
  const yInferior = 170;

  const leds = Math.min(res.ledsPorRama, 4); // Dibujar hasta 4 visualmente
  const espaciadoLeds = 50;

  let ledsSvg = "";
  for (let i = 0; i < leds; i++) {
    const x = xLedInicio + (i * espaciadoLeds);
    ledsSvg += `
      <!-- Conexión previa -->
      <line x1="${x - 18}" y1="${ySuperior}" x2="${x - 8}" y2="${ySuperior}" stroke="#94a3b8" stroke-width="2" />
      
      <!-- Símbolo Diodo LED -->
      <polygon points="${x - 8},${ySuperior - 10} ${x - 8},${ySuperior + 10} ${x + 8},${ySuperior}" fill="${colorHex}" stroke="#f8fafc" stroke-width="1.5" />
      <line x1="${x + 8}" y1="${ySuperior - 10}" x2="${x + 8}" y2="${ySuperior + 10}" stroke="#f8fafc" stroke-width="2" />
      
      <!-- Flechas de emisión de luz del LED -->
      <line x1="${x}" y1="${ySuperior - 12}" x2="${x + 8}" y2="${ySuperior - 20}" stroke="${colorHex}" stroke-width="1.5" marker-end="url(#flecha-luz)" />
      <line x1="${x + 6}" y1="${ySuperior - 10}" x2="${x + 14}" y2="${ySuperior - 18}" stroke="${colorHex}" stroke-width="1.5" marker-end="url(#flecha-luz)" />
      
      <text x="${x}" y="${ySuperior + 24}" fill="#cbd5e1" font-size="10" text-anchor="middle">LED ${i + 1}</text>
    `;
  }

  const xFinalRama = xLedInicio + ((leds - 1) * espaciadoLeds) + 8;
  const xRetorno = Math.max(xFinalRama + 35, 460);

  const svg = `
    <svg viewBox="0 0 ${ancho} ${alto}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <marker id="flecha-luz" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse">
          <path d="M 0 2 L 8 5 L 0 8 z" fill="${colorHex}" />
        </marker>
      </defs>

      <!-- Fuente de Alimentación Vcc -->
      <circle cx="${xFuente}" cy="${ySuperior}" r="4" fill="#38bdf8" />
      <circle cx="${xFuente}" cy="${yInferior}" r="4" fill="#64748b" />
      
      <!-- Líneas de la fuente DC -->
      <line x1="${xFuente - 12}" y1="${(ySuperior + yInferior)/2 - 8}" x2="${xFuente + 12}" y2="${(ySuperior + yInferior)/2 - 8}" stroke="#38bdf8" stroke-width="3" />
      <line x1="${xFuente - 6}" y1="${(ySuperior + yInferior)/2 + 8}" x2="${xFuente + 6}" y2="${(ySuperior + yInferior)/2 + 8}" stroke="#64748b" stroke-width="2" />
      <line x1="${xFuente}" y1="${ySuperior}" x2="${xFuente}" y2="${(ySuperior + yInferior)/2 - 8}" stroke="#94a3b8" stroke-width="2" />
      <line x1="${xFuente}" y1="${(ySuperior + yInferior)/2 + 8}" x2="${xFuente}" y2="${yInferior}" stroke="#94a3b8" stroke-width="2" />
      <text x="${xFuente - 20}" y="${(ySuperior + yInferior)/2 - 4}" fill="#38bdf8" font-size="11" font-weight="bold">+</text>
      <text x="${xFuente - 20}" y="${(ySuperior + yInferior)/2 + 14}" fill="#94a3b8" font-size="11" font-weight="bold">-</text>
      <text x="${xFuente - 28}" y="${(ySuperior + yInferior)/2 + 4}" fill="#f8fafc" font-size="11" font-weight="bold" text-anchor="end">V<sub>cc</sub>: ${res.vFuente}V</text>

      <!-- Conductor hacia Resistencia -->
      <line x1="${xFuente}" y1="${ySuperior}" x2="${xRes - 25}" y2="${ySuperior}" stroke="#94a3b8" stroke-width="2" />

      <!-- Símbolo Resistencia Limitadora R -->
      <rect x="${xRes - 22}" y="${ySuperior - 10}" width="44" height="20" fill="#1e293b" stroke="#f59e0b" stroke-width="2" rx="3" />
      <text x="${xRes}" y="${ySuperior + 4}" fill="#f59e0b" font-size="11" font-weight="bold" text-anchor="middle">R</text>
      <text x="${xRes}" y="${ySuperior - 16}" fill="#f59e0b" font-size="11" font-weight="bold" text-anchor="middle">${res.rComercial} Ω</text>
      <text x="${xRes}" y="${ySuperior + 26}" fill="#94a3b8" font-size="9" text-anchor="middle">(${res.pComercialW} W)</text>

      <!-- Conductor de Resistencia hacia LEDs -->
      <line x1="${xRes + 22}" y1="${ySuperior}" x2="${xLedInicio - 18}" y2="${ySuperior}" stroke="#94a3b8" stroke-width="2" />

      <!-- Símbolos LEDs -->
      ${ledsSvg}

      <!-- Conductor de retorno al polo negativo (GND) -->
      <line x1="${xFinalRama}" y1="${ySuperior}" x2="${xRetorno}" y2="${ySuperior}" stroke="#94a3b8" stroke-width="2" />
      <line x1="${xRetorno}" y1="${ySuperior}" x2="${xRetorno}" y2="${yInferior}" stroke="#94a3b8" stroke-width="2" />
      <line x1="${xRetorno}" y1="${yInferior}" x2="${xFuente}" y2="${yInferior}" stroke="#94a3b8" stroke-width="2" />

      <!-- Información del Circuito -->
      <text x="${(xFuente + xRetorno) / 2}" y="${yInferior - 10}" fill="#38bdf8" font-size="11" text-anchor="middle">Corriente real de rama: I = ${res.ifRealMa.toFixed(2)} mA | Eficiencia: ${res.eficienciaPct.toFixed(1)}%</text>
    </svg>
  `;

  contenedor.innerHTML = svg;
}

