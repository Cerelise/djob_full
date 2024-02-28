<template>
  <n-layout>
    <n-layout-header>
      <HeaderVue class="h-[10vh] shadow-md" />
    </n-layout-header>
    <n-layout has-sider class="bg-[#F5F5F5] max-h-[90vh]">
      <AsideVue />
      <router-view v-slot="{ Component }">
        <transition name="fade">
          <component :is="Component"></component>
        </transition>
      </router-view>
    </n-layout>
  </n-layout>
</template>

<script setup>
import AsideVue from "./aside.vue";
import HeaderVue from "./header.vue";
</script>

<style lang="scss" scoped>
.fade-enter-from {
  opacity: 0;
  -webkit-transform: translate3d(0, -100%, 0);
  transform: translate3d(0, -100%, 0);
}
.fade-enter-to {
  opacity: 1;
  -webkit-transform: translate3d(0, 0, 0);
  transform: translate3d(0, 0, 0);
}
.fade-leave-from {
  opacity: 1;
}
.fade-leave-to {
  opacity: 0;
  -webkit-transform: translate3d(0, 100%, 0);
  transform: translate3d(0, 100%, 0);
}
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s;
}
.fade-enter-active {
  transition-delay: 0.3s;
}
</style>
