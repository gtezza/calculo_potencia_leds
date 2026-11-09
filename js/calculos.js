/**
 * Módulo de cálculos matemáticos, fotométricos y radiométricos para LEDs.
 * Basado en la Clase 5: Cálculos de potencia emitida por los LEDs.
 */

const KM_CIE = 683.0; // lm/W (Eficacia máxima CIE a 555 nm)

// Tabla de datos fotópicos CIE y parámetros típicos de LEDs (Slide 15 y 20)
const TABLA_LEDS_CIE = {
  rojo_660: {
    nombre: "Rojo profundo / Fotobiomodulación (660 nm)",
    longitudOnda: 660,
    vLambda: 0.0610,
    factorLmW: 41.6,
    colorHex: "#e63946",
    mcdDefecto: 5000,
    anguloDefecto: 30,
    distanciaDefecto: 2.0,
    vfTipico: 2.0,
    wpeTipico: 0.20
  },
  rojo_625: {
    nombre: "Rojo estándar (625 nm)",
    longitudOnda: 625,
    vLambda: 0.3210,
    factorLmW: 219.2,
    colorHex: "#ff4d4d",
    mcdDefecto: 4500,
    anguloDefecto: 30,
    distanciaDefecto: 2.0,
    vfTipico: 2.0,
    wpeTipico: 0.18
  },
  amarillo_590: {
    nombre: "Amarillo / Ámbar (590 nm)",
    longitudOnda: 590,
    vLambda: 0.7570,
    factorLmW: 517.0,
    colorHex: "#ffb703",
    mcdDefecto: 4000,
    anguloDefecto: 30,
    distanciaDefecto: 2.0,
    vfTipico: 2.1,
    wpeTipico: 0.11
  },
  verde_555: {
    nombre: "Verde pico CIE (555 nm)",
    longitudOnda: 555,
    vLambda: 1.0000,
    factorLmW: 683.0,
    colorHex: "#52b788",
    mcdDefecto: 9000,
    anguloDefecto: 25,
    distanciaDefecto: 2.0,
    vfTipico: 3.2,
    wpeTipico: 0.08
  },
  verde_525: {
    nombre: "Verde estándar (525 nm)",
    longitudOnda: 525,
    vLambda: 0.7930,
    factorLmW: 541.6,
    colorHex: "#2a9d8f",
    mcdDefecto: 8000,
    anguloDefecto: 20,
    distanciaDefecto: 2.0,
    vfTipico: 3.2,
    wpeTipico: 0.085
  },
  azul_465: {
    nombre: "Azul espectral (465 nm)",
    longitudOnda: 465,
    vLambda: 0.0739,
    factorLmW: 50.5,
    colorHex: "#219ebc",
    mcdDefecto: 14000,
    anguloDefecto: 30,
    distanciaDefecto: 2.0,
    vfTipico: 3.2,
    wpeTipico: 0.22
  },
  uva_395: {
    nombre: "UV-A cercano (395 nm)",
    longitudOnda: 395,
    vLambda: 0.0002,
    factorLmW: 0.13,
    colorHex: "#7209b7",
    mcdDefecto: 500,
    anguloDefecto: 25,
    distanciaDefecto: 2.0,
    vfTipico: 3.4,
    wpeTipico: 0.13
  },
  uva_365: {
    nombre: "UV-A profundo (365 nm)",
    longitudOnda: 365,
    vLambda: 0.000011,
    factorLmW: 0.0075,
    colorHex: "#3a0ca3",
    mcdDefecto: 100,
    anguloDefecto: 30,
    distanciaDefecto: 2.0,
    vfTipico: 3.6,
    wpeTipico: 0.05
  }
};

/**
 * Obtiene o aproxima el valor de sensibilidad fotópica V(lambda) CIE 1931.
 */
function obtenerVLambda(longitudOndaNm) {
  for (const clave in TABLA_LEDS_CIE) {
    if (Math.abs(TABLA_LEDS_CIE[clave].longitudOnda - longitudOndaNm) <= 2) {
      return TABLA_LEDS_CIE[clave].vLambda;
    }
  }
  if (longitudOndaNm < 380 || longitudOndaNm > 750) {
    return 0.0;
  }
  return Math.exp(-0.5 * Math.pow((longitudOndaNm - 555.0) / 45.0, 2));
}

/**
 * PASO 1: Conversión de Milicandelas a Lúmenes.
 */
function calcularPaso1(intensidadMcd, anguloTotalGrados) {
  const semiAnguloGrados = anguloTotalGrados / 2.0;
  const semiAnguloRad = (semiAnguloGrados * Math.PI) / 180.0;
  const anguloSolidoSr = 2.0 * Math.PI * (1.0 - Math.cos(semiAnguloRad));
  const intensidadCd = intensidadMcd / 1000.0;
  const flujoLumenes = intensidadCd * anguloSolidoSr;

  return {
    intensidadMcd,
    intensidadCd,
    anguloTotalGrados,
    semiAnguloGrados,
    anguloSolidoSr,
    flujoLumenes
  };
}

/**
 * PASO 2: Conversión de Lúmenes a Potencia Óptica en mW.
 */
function calcularPaso2(flujoLumenes, longitudOndaNm) {
  const vLambda = obtenerVLambda(longitudOndaNm);
  const factorEficacia = KM_CIE * vLambda;
  let potenciaOpticaW = 0.0;
  let potenciaOpticaMw = 0.0;

  if (factorEficacia > 0) {
    potenciaOpticaW = flujoLumenes / factorEficacia;
    potenciaOpticaMw = potenciaOpticaW * 1000.0;
  }

  return {
    flujoLumenes,
    longitudOndaNm,
    vLambda,
    factorEficaciaLmW: factorEficacia,
    potenciaOpticaW,
    potenciaOpticaMw
  };
}

/**
 * Cálculo de geometría a la distancia especificada (d).
 */
function calcularGeometria(distanciaCm, semiAnguloGrados) {
  const semiAnguloRad = (semiAnguloGrados * Math.PI) / 180.0;
  const radioCm = distanciaCm * Math.tan(semiAnguloRad);
  let areaCm2 = 0.0;

  if (distanciaCm === 0) {
    areaCm2 = 0.15; // Contacto directo con piel (~área de lente de 5mm)
  } else {
    areaCm2 = Math.PI * Math.pow(radioCm, 2);
  }

  return {
    distanciaCm,
    radioCm,
    areaCm2
  };
}

/**
 * Cálculo de Irradiancia y Dosis.
 */
function calcularIrradianciaYDosis(potenciaOpticaMw, areaCm2, tiempoSegundos) {
  const irradianciaMwCm2 = areaCm2 > 0 ? potenciaOpticaMw / areaCm2 : 0;
  const dosisJCm2 = (irradianciaMwCm2 * tiempoSegundos) / 1000.0;

  const tiemposTabla = [
    { label: "1 min (60 s)", segs: 60 },
    { label: "5 min (300 s)", segs: 300 },
    { label: "10 min (600 s)", segs: 600 },
    { label: "15 min (900 s)", segs: 900 },
    { label: "20 min (1200 s)", segs: 1200 }
  ];

  const tablaDosis = tiemposTabla.map(t => ({
    etiqueta: t.label,
    dosis: (irradianciaMwCm2 * t.segs) / 1000.0
  }));

  return {
    irradianciaMwCm2,
    tiempoSegundos,
    dosisJCm2,
    tablaDosis
  };
}

