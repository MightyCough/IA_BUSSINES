<template>
  <div class="artefactos-panel">
    <div class="artefactos-grid">
      <div
        v-for="item in artefactos"
        :key="item.titulo"
        class="artefacto-card"
        :class="{ destacado: item.destacado }"
        tabindex="0"
        role="button"
        style="cursor:pointer;"
      >
        <div class="flip-card-inner">
          <div class="flip-card-front">
            <div class="artefacto-img-bg">
              <img :src="item.imagen" :alt="item.titulo" class="artefacto-img-full" />
              <div class="artefacto-titulo-overlay">
                {{ item.titulo }}
              </div>
            </div>
          </div>
          <div class="flip-card-back">
            <div class="artefacto-desc">{{ item.descripcion }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const artefactos = [
  {
    titulo: 'Generacion de ideas',
    descripcion: 'Sugerencias personalizadas según tendencias del mercado y tus recursos disponibles',
    imagen: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHwqGPU-W4um6vgBmE1AVkm3Lt0eDVTyamWA&s',
  },
  {
    titulo: 'Plan de Negocio Guiado',
    descripcion: 'Canvas, Lean Startup, análisis SWOT y más herramientas con explicaciones paso a paso',
    destacado: true,
    imagen: 'https://cdn.forbes.com.mx/2024/07/emprender_negocios-640x360.jpg',
  },
  {
    titulo: 'Asesoría en Marketing',
    descripcion: 'Estrategias para redes sociales, publicidad digital y posicionamiento SEO',
    imagen: 'https://einatec.com/wp-content/uploads/2019/06/marketing-para-asesorias.jpg',
  },
  {
    titulo: 'Gestión Financiera',
    descripcion: 'Proyecciones simples, punto de equilibrio y análisis de costos básicos',
    imagen: 'https://b2676882.smushcdn.com/2676882/wp-content/uploads/2025/02/gestion-financiera-con-Excel-1050x500.jpg?lossy=1&strip=1&webp=1',
  },
  {
    titulo: 'Capacitación Continua',
    descripcion: 'Aprende sobre ventas, liderazgo y finanzas con lenguaje sencillo y ejemplos prácticos',
    imagen: 'https://universidadeuropea.com/resources/media/images/que-es-formacion-continua-800x450.original.jpg',
  },
  {
    titulo: 'Seguimiento de Progreso',
    descripcion: 'Recordatorios inteligentes y métricas de avance para mantener tu momentum',
    imagen: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTPh4orQdVHaCOL3tlqYk5_XuuuoLWN2uwbQw&s',
  },
];

function handleArtefactoClick(item) {
  // Aquí se puede manejar la navegación o acción al hacer clic
  // Por ahora solo mostramos en consola
  console.log('Artefacto seleccionado:', item.titulo);
}
</script>

<style scoped>

.artefactos-panel {
  width: 100%;
  min-height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 0 0 0;
}

.artefactos-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  column-gap: 56px;
  row-gap: 40px;
  justify-items: center;
  width: 100%;
  max-width: 900px;
}
.artefacto-card {
  background: transparent;
  border-radius: 18px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.07);
  padding: 0;
  min-width: 240px;
  max-width: 370px;
  width: 100%;
  text-align: left;
  border: 1.2px solid #a78bfa;
  transition: box-shadow 0.18s, border 0.18s, transform 0.18s;
  overflow: hidden;
}
.artefacto-card:hover, .artefacto-card:focus {
  border: 2px solid #7c3aed;
  box-shadow: 0 8px 28px rgba(124,58,237,0.13);
  transform: translateY(-6px) scale(1.03);
  outline: none;
}
.artefacto-card.destacado {
  /* Sin borde especial */
}
/* Flip card styles */
.flip-card-inner {
  position: relative;
  width: 100%;
  height: 180px;
  transition: transform 0.6s cubic-bezier(.4,2,.6,1);
  transform-style: preserve-3d;
}
.artefacto-card:hover .flip-card-inner,
.artefacto-card:focus .flip-card-inner {
  transform: rotateY(180deg);
}
.flip-card-front, .flip-card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  border-radius: 18px;
  overflow: hidden;
}
.flip-card-front {
  background: transparent;
  z-index: 2;
  padding: 0;
  display: flex;
  align-items: stretch;
  justify-content: stretch;
}
.flip-card-back {
  background: #f8f7fd;
  transform: rotateY(180deg);
  color: #444;
  padding: 18px 18px 10px 18px;
  text-align: center;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
}
.artefacto-img-bg {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: flex-end;
  justify-content: stretch;
}
.artefacto-img-full {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.artefacto-titulo-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  background: rgba(40, 0, 80, 0.55);
  color: #fff;
  font-size: 1.15rem;
  font-weight: 700;
  padding: 14px 0 10px 0;
  text-align: center;
  letter-spacing: 0.01em;
  border-radius: 0 0 18px 18px;
}
.artefacto-desc {
  font-size: 1rem;
  color: #444;
}
@media (max-width: 900px) {
  .artefactos-grid {
    grid-template-columns: 1fr;
    gap: 20px;
    max-width: 400px;
  }
  .artefactos-panel {
    align-items: flex-start;
    padding-top: 24px;
  }
}
</style>