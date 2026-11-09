/**
 * Módulo de cálculo y visualización de Array / Matriz de LEDs para Fototerapia.
 * Calcula potencia óptica acumulada, lúmenes totales, superposición de conos y dosimetría de panel.
 */

function calcularArrayLeds(config) {
  const {
    potenciaUnLedMw,
    flujoLumenesUnLed,
    semiAnguloGrados,
    distanciaCm,
    filas,
    columnas,
    espaciadoPitchCm,
    dosisObjetivoJCm2
  } = config;

  const totalLeds = (filas || 1) * (columnas || 1);
  const potenciaTotalMw = potenciaUnLedMw * totalLeds;
  const potenciaTotalW = potenciaTotalMw / 1000.0;
  const lumenesTotales = flujoLumenesUnLed * totalLeds;

  // Geometría del cono de un solo LED
  const semiAnguloRad = (semiAnguloGrados * Math.PI) / 180.0;
  const radioConoCm = distanciaCm * Math.tan(semiAnguloRad);
  const diametroConoCm = 2.0 * radioConoCm;

  // Superposición: si el diámetro del haz supera la separación entre centros de LEDs
  const pitch = espaciadoPitchCm || 1.5;
  const haySolapamiento = diametroConoCm > pitch;
  const factorSolapamiento = pitch > 0 ? diametroConoCm / pitch : 1.0;

  // Dimensiones del panel emisor
  const anchoPanelFisicoCm = (columnas > 1 ? (columnas - 1) * pitch : pitch) + pitch;
  const altoPanelFisicoCm = (filas > 1 ? (filas - 1) * pitch : pitch) + pitch;
  const areaFisicaPanelCm2 = anchoPanelFisicoCm * altoPanelFisicoCm;

  // Área proyectada efectiva en el plano a distancia d (con expansión del haz perimetral)
  const anchoEfectivoCm = anchoPanelFisicoCm + (2.0 * radioConoCm);
  const altoEfectivoCm = altoPanelFisicoCm + (2.0 * radioConoCm);
  const areaEfectivaCm2 = anchoEfectivoCm * altoEfectivoCm;

  // Irradiancia media del array
  const irradianciaArrayMwCm2 = areaEfectivaCm2 > 0 ? potenciaTotalMw / areaEfectivaCm2 : 0;

  // Comparativa de tiempos de aplicación para alcanzar la dosis objetivo (ej: 4 J/cm²)
  const objetivo = dosisObjetivoJCm2 || 4.0;
  // Irradiancia de 1 solo LED a distancia d
  const areaUnLed = distanciaCm === 0 ? 0.15 : Math.PI * Math.pow(radioConoCm, 2);
  const irradianciaUnLed = areaUnLed > 0 ? potenciaUnLedMw / areaUnLed : 0;

  const tiempoUnLedSeg = irradianciaUnLed > 0 ? (objetivo * 1000.0) / irradianciaUnLed : 0;
  const tiempoArraySeg = irradianciaArrayMwCm2 > 0 ? (objetivo * 1000.0) / irradianciaArrayMwCm2 : 0;
  const aceleracion = tiempoArraySeg > 0 ? tiempoUnLedSeg / tiempoArraySeg : 1.0;

  return {
    filas,
    columnas,
    totalLeds,
    pitchCm: pitch,
    potenciaTotalMw,
    potenciaTotalW,
    lumenesTotales,
    radioConoCm,
    diametroConoCm,
    haySolapamiento,
    factorSolapamiento,
    anchoPanelFisicoCm,
    altoPanelFisicoCm,
    areaFisicaPanelCm2,
    anchoEfectivoCm,
    altoEfectivoCm,
    areaEfectivaCm2,
    irradianciaArrayMwCm2,
    dosisObjetivoJCm2: objetivo,
    irradianciaUnLed,
    tiempoUnLedSeg,
    tiempoArraySeg,
    aceleracion
  };
}

/**
 * Renderiza el gráfico interactivo de la matriz de LEDs y sus halos de luz.
 */
function dibujarMatrizLedsSVG(datos, colorHex = "#e63946") {
  const contenedor = document.getElementById("contenedor-svg-matriz");
  if (!contenedor) return;

  const anchoSvg = 540;
  const altoSvg = 260;
  const filas = Math.min(datos.filas, 8);
  const columnas = Math.min(datos.columnas, 12);

  const margenX = 70;
  const margenY = 50;
  const pasoX = (anchoSvg - 2 * margenX) / (columnas > 1 ? columnas - 1 : 1);
  const pasoY = (altoSvg - 2 * margenY) / (filas > 1 ? filas - 1 : 1);

  // Escala visual del halo luminoso proporcional al solapamiento
  const radioHaloPx = Math.min(Math.max(pasoX * (datos.factorSolapamiento / 2), 12), 48);

  let ledsSvg = "";
  for (let f = 0; f < filas; f++) {
    for (let c = 0; c < columnas; c++) {
      const cx = margenX + (c * pasoX);
      const cy = margenY + (f * pasoY);
      ledsSvg += `
        <!-- Halo luminoso con superposición -->
        <circle cx="${cx}" cy="${cy}" r="${radioHaloPx}" fill="${colorHex}" fill-opacity="${datos.haySolapamiento ? 0.18 : 0.08}" stroke="${colorHex}" stroke-width="0.8" stroke-dasharray="2,2" />
        <!-- Chip LED -->
        <circle cx="${cx}" cy="${cy}" r="6" fill="${colorHex}" filter="drop-shadow(0 0 5px ${colorHex})" stroke="#fff" stroke-width="1.2" />
      `;
    }
  }

  const svg = `
    <svg viewBox="0 0 ${anchoSvg} ${altoSvg}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <!-- Fondo y marco del panel emisor -->
      <rect x="${margenX - 25}" y="${margenY - 25}" width="${(columnas - 1) * pasoX + 50}" height="${(filas - 1) * pasoY + 50}" rx="10" fill="#0b1120" stroke="#334155" stroke-width="1.5" />
      
      <!-- Cuadrícula de LEDs y halos -->
      ${ledsSvg}

      <!-- Indicadores de cotas del panel -->
      <text x="${anchoSvg / 2}" y="20" fill="#f8fafc" font-size="12" font-weight="bold" text-anchor="middle">Matriz de ${datos.filas} × ${datos.columnas} = ${datos.totalLeds} LEDs (${datos.pitchCm.toFixed(1)} cm pitch)</text>
      <text x="${anchoSvg / 2}" y="${altoSvg - 10}" fill="${datos.haySolapamiento ? '#10b981' : '#f59e0b'}" font-size="11" font-weight="bold" text-anchor="middle">
        ${datos.haySolapamiento ? '✔ Solapamiento de conos activo (Haz uniforme y homogéneo)' : 'ℹ Conos aislados (Aumenta la distancia d para solapar los haces)'}
      </text>
    </svg>
  `;

  contenedor.innerHTML = svg;
}

