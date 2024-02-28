<template>
  <n-empty v-if="data?.length == 0" />
  <n-collapse :trigger-areas="['main', 'arrow']" accordion v-else>
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
        <n-button type="success" @click="pass(item.id)">通过</n-button>
        <n-button type="error" class="ml-5" @click="repulse(item.id)"
          >作废</n-button
        >
      </template>
    </n-collapse-item>
  </n-collapse>
</template>

<script setup>
import { getApprovalsApi, passCompApi } from "@/api";
import { ref, onMounted } from "vue";

const data = ref([]);

function getData() {
  getApprovalsApi("company").then((res) => {
    console.log(res);
    data.value = res;
  });
}
function pass(id) {
  passCompApi(id, { status: 1, message: "" }).then((res) => getData());
}
function repulse(id) {
  passCompApi(id, { status: 0, message: "招聘信息不符合要求!" }).then((res) =>
    getData()
  );
}
onMounted(() => getData());
</script>

<style lang="scss" scoped></style>
