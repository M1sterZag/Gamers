<template>
  <section class="w-full grid grid-cols-[282px_1fr] gap-[82px] min-h-screen">
    <!-- Сайдбар -->
    <div class="sticky top-0 h-screen">
      <SideBar/>
    </div>
    <!-- Основной контент -->
    <div class="overflow-y-auto">
      <router-view/>
    </div>
  </section>
</template>

<script setup>
import SideBar from '@/components/SideBar.vue'
</script>