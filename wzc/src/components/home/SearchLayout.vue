<template>
  <div class="w-full h-full flex justify-center items-center pt-40 flex-col">
    <div class="text-4xl">{{ title }}</div>
    <div class="w-5/12 py-5 pb-10">
      <n-input
        round
        placeholder="搜索"
        autofocus
        @keyup.enter.native="handleEnter"
        v-model:value="key"
      >
        <template #suffix>
          <n-button
            icon-placement="left"
            secondary
            strong
            circle
            class="w-20"
            type="warning"
            @click="handleEnter"
          >
            <template #icon>
              <n-icon>
                <SearchSharp />
              </n-icon>
            </template>
            搜索
          </n-button>
        </template>
      </n-input>
      <div class="pt-5">
        <n-row :gutter="30">
          <n-col :span="12">
            <n-input
              pair
              separator="-"
              :placeholder="['最小薪资', '最大薪资']"
              clearable
              @update:value="(e) => (minAndMax = e)"
              type="number"
            />
          </n-col>
          <n-col :span="12">
            <n-select multiple v-model:value="value" :options="tags" />
          </n-col>
        </n-row>
      </div>
    </div>

    <div class="w-9/12">
      <JobItem v-for="item in data" :show="show" :item="item" />
    </div>
  </div>
</template>

<script setup>
import { SearchSharp } from "@vicons/material";
import JobItem from "./JobItem.vue";
import { ref } from "vue";
import { getJobsApi, getTagsApi } from "@/api";

defineProps({
  title: {
    type: String,
    default: "Jobs",
  },
  api: {
    type: String,
    default: "search-job",
  },
});

const tags = ref([]);

function getTags() {
  getTagsApi().then((res) => {
    tags.value = res.split(",").map((t) => ({ label: t, value: t }));
  });
}

const value = ref([]);
const minAndMax = ref([]);
const key = ref();
const data = ref([]);

function getData() {
  const params = {
    keyword: key.value,
    min_salary: minAndMax.value[0],
    max_salary: minAndMax.value[1],
    category: [...value.value].join(","),
  };
  getJobsApi(params).then((res) => {
    data.value = res.data;
  });
}

function handleEnter() {
  getData();
}
getData();
getTags();
</script>

<style lang="scss" scoped></style>
