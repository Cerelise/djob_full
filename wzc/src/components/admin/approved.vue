<template>
  <n-empty v-if="data.length == 0" />
  <n-collapse accordion v-else>
    <n-collapse-item
      :title="item.title"
      :name="item.id"
      v-for="item in data"
      class="cursor-default"
    >
      <div>工作分类: {{ item.category }}</div>
      <div>发布公司: {{ item.company_name }}</div>
      <div>公司地址: {{ item.location }}</div>
      <div>工作描述: {{ item.description }}</div>
      <div>发布时间: {{ item.created_at }}</div>
      <template #header-extra>
        <n-tag type="success" v-if="item.status == 1"> 已通过 </n-tag>
        <n-tag type="error" v-else> 已打回 </n-tag>
      </template>
    </n-collapse-item>
  </n-collapse>
</template>

<script setup>
import { getApprovalsApi } from "@/api";
import { ref, onMounted } from "vue";

const data = ref([]);
function getData() {
  getApprovalsApi("all").then((res) => {
    data.value = res;
  });
}
onMounted(() => getData());
</script>

<style lang="scss" scoped></style>
