<template>
  <div>
    <HeaderVue />
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component class="pt-14" :is="Component"></component>
      </transition>
    </router-view>
  </div>
</template>

<script setup>
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
