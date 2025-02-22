<template>
  <section class="w-full grid grid-cols-[282px_1fr] gap-[82px] min-h-screen">
    <SideBar/>
    <router-view/>
  </section>
</template>

<script setup>
import SideBar from '@/components/SideBar.vue'
</script>
