<template>
  <nav class="navbar">
    <div class="navbar-brand">
      <h1>StarNow</h1>
    </div>
    <div class="navbar-links">
      <a href="#features" @click="scrollToSection('features')">Lo que ofrecemos</a>
      <a href="#how-it-works" @click="scrollToSection('how-it-works')">Como funciona</a>
      <a href="#testimonials" @click="scrollToSection('testimonials')">Testimonios</a>
    </div>
    <div class="navbar-buttons">
      <n-button quaternary @click="$router.push('/login')">Iniciar Sesion</n-button>
      <n-button type="primary" @click="$router.push('/register')">Registrar</n-button>
    </div>
  </nav>
</template>

<script setup>
const scrollToSection = (sectionId) => {
  const element = document.getElementById(sectionId)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' })
  }
}
</script>

<style scoped>
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.5rem 2rem;
  background: #fff;
  border-bottom: 1px solid #eee;
}
.navbar-brand h1 {
  font-weight: bold;
  font-size: 1.5rem;
  margin: 0;
}
.navbar-links {
  display: flex;
  gap: 2rem;
  list-style: none;
  margin: 0;
  padding: 0;
}
.navbar-links a {
  color: #4a5568;
  text-decoration: none;
  padding: 8px 16px;
  transition: color 0.3s ease;
  font-weight: 500;
}
.navbar-links a:hover {
  color: #a855f7;
}
.navbar-buttons {
  display: flex;
  gap: 0.5rem;
}

/* Añade un efecto suave al scroll */
html {
  scroll-behavior: smooth;
}
</style>