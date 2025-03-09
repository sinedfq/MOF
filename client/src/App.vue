<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <div class="">
      <nav>
        <RouterLink to="/">
          <label class = "custom-button">Главная</label>
        </RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<!-- Подключаем стили -->
<style scoped>
@import '@/assets/base.css';
</style>
