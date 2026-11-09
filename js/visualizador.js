/**
 * Módulo de visualización gráfica en SVG del haz del LED.
 * Muestra el cono de radiación, el ángulo de apertura, la distancia d y la huella proyectada.
 */

function actualizarVisualizador(datos) {
  const contenedor = document.getElementById("contenedor-svg");
  if (!contenedor) return;

  const { semiAnguloGrados, distanciaCm, radioCm, colorHex, longitudOndaNm } = datos;

  const anchoSvg = 540;
  const altoSvg = 340;
  
  const ledX = anchoSvg / 2;
  const ledY = 40;
  
  // Escala para mapear la distancia física en cm a píxeles
  const planoY = 270;
  const alturaConoPx = planoY - ledY;
  
  // Limitar visualmente el ángulo para que no desborde el lienzo SVG
  const semiAnguloVisual = Math.min(Math.max(semiAnguloGrados, 5), 65);
  const semiAnguloRad = (semiAnguloVisual * Math.PI) / 180.0;
  const radioVisualPx = Math.min(alturaConoPx * Math.tan(semiAnguloRad), 220);

  const xIzquierda = ledX - radioVisualPx;
  const xDerecha = ledX + radioVisualPx;

  const colorPrincipal = colorHex || "#e63946";

  const svgContent = `
    <svg viewBox="0 0 ${anchoSvg} ${altoSvg}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="overflow: visible;">
      <defs>
        <!-- Gradiente del cono de luz -->
        <linearGradient id="gradienteCono" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="${colorPrincipal}" stop-opacity="0.85" />
          <stop offset="60%" stop-color="${colorPrincipal}" stop-opacity="0.35" />
          <stop offset="100%" stop-color="${colorPrincipal}" stop-opacity="0.12" />
        </linearGradient>
        
        <!-- Marcador de flecha para cotas -->
        <marker id="flecha" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#94a3b8" />
        </marker>
      </defs>

      <!-- Cuadrícula tenue de fondo -->
      <line x1="40" y1="${planoY}" x2="${anchoSvg - 40}" y2="${planoY}" stroke="#334155" stroke-dasharray="4,4" stroke-width="1.5" />
      <line x1="${ledX}" y1="20" x2="${ledX}" y2="${planoY + 30}" stroke="#475569" stroke-dasharray="3,3" stroke-width="1" />

      <!-- Cono de emisión luminosa -->
      <polygon points="${ledX},${ledY} ${xIzquierda},${planoY} ${xDerecha},${planoY}" fill="url(#gradienteCono)" stroke="${colorPrincipal}" stroke-width="1.8" stroke-dasharray="6,3" />

      <!-- Huella elíptica/circular proyectada en la superficie -->
      <ellipse cx="${ledX}" cy="${planoY}" rx="${radioVisualPx}" ry="${radioVisualPx * 0.28}" fill="${colorPrincipal}" fill-opacity="0.3" stroke="${colorPrincipal}" stroke-width="2" />

      <!-- Encabezado del LED emisor -->
      <circle cx="${ledX}" cy="${ledY - 14}" r="14" fill="${colorPrincipal}" filter="drop-shadow(0 0 8px ${colorPrincipal})" />
      <path d="M ${ledX - 10} ${ledY - 14} L ${ledX + 10} ${ledY - 14} L ${ledX} ${ledY} Z" fill="#f8fafc" opacity="0.9" />
      <text x="${ledX}" y="${ledY - 22}" fill="#f8fafc" font-size="12" font-weight="bold" text-anchor="middle">LED (${longitudOndaNm} nm)</text>

      <!-- Indicador de semi-ángulo θ_1/2 -->
      <path d="M ${ledX} ${ledY + 45} A 45 45 0 0 1 ${ledX + 45 * Math.sin(semiAnguloRad)} ${ledY + 45 * Math.cos(semiAnguloRad)}" fill="none" stroke="#f1f5f9" stroke-width="1.5" />
      <text x="${ledX + 22}" y="${ledY + 42}" fill="#f1f5f9" font-size="11" font-weight="600">θ = ${semiAnguloGrados.toFixed(1)}°</text>

      <!-- Cota de distancia d -->
      <line x1="${ledX - radioVisualPx - 25}" y1="${ledY}" x2="${ledX - radioVisualPx - 25}" y2="${planoY}" stroke="#94a3b8" stroke-width="1.5" marker-start="url(#flecha)" marker-end="url(#flecha)" />
      <text x="${ledX - radioVisualPx - 32}" y="${(ledY + planoY) / 2}" fill="#cbd5e1" font-size="12" font-weight="bold" text-anchor="end" dominant-baseline="middle">d = ${distanciaCm.toFixed(2)} cm</text>

      <!-- Cota del radio de la huella r -->
      <line x1="${ledX}" y1="${planoY + 22}" x2="${xDerecha}" y2="${planoY + 22}" stroke="#38bdf8" stroke-width="1.5" marker-start="url(#flecha)" marker-end="url(#flecha)" />
      <text x="${ledX + radioVisualPx / 2}" y="${planoY + 38}" fill="#38bdf8" font-size="11" font-weight="bold" text-anchor="middle">r = ${radioCm.toFixed(3)} cm</text>

      <!-- Etiqueta de plano iluminado -->
      <text x="${anchoSvg - 45}" y="${planoY - 8}" fill="#94a3b8" font-size="11" text-anchor="end">Superficie iluminada</text>
    </svg>
  `;

  contenedor.innerHTML = svgContent;
}
