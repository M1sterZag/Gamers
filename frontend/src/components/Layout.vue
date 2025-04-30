<template>
  <div class="w-full min-h-screen flex flex-col lg:flex-row">
    <!-- Сайдбар - только для десктопа -->
    <div class="hidden wide:block sticky top-0 h-screen">
      <SideBar/>
    </div>
    <!-- Мобильная навигация - для устройств с шириной менее 1440px -->
    <div class="wide:hidden">
      <MobileNav/>
    </div>
    <!-- Основной контент -->
    <main
        class="flex-1 wide:ml-[80px] px-4 wide:px-0 wide:pr-[64px] pb-20 wide:pb-[20px] pt-16 wide:pt-[88px] overflow-y-auto"
    >
      <router-view/>
    </main>
  </div>
</template>

<script setup>
import SideBar from '@/components/SideBar.vue';
import MobileNav from '@/components/MobileNav.vue';
</script>