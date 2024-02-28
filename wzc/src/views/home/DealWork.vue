<template>
  <div class="w-full h-full flex justify-center items-center pt-40 flex-col">
    <div class="text-4xl">处理工作</div>
    <div class="w-7/12 py-5 pb-10">
      <WorkItem v-for="item in data" :item="item" @reload="reload" />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { getAppliesEmployerApi } from "@/api";
import WorkItem from "@/components/home/WorkItem.vue";
const data = ref([]);

function reload() {
  getAppliesEmployerApi().then((res) => (data.value = res.data));
}
reload();
</script>

<style lang="scss" scoped></style>
