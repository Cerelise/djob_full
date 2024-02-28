<template>
  <div
    class="flex justify-center items-center bg-[#FAF9F9] flex-col cursor-default"
  >
    <div class="py-5 px-32 flex justify-between items-center w-full bg-white">
      <div class="flex items-center">
        <div class="text-3xl font-bold">{{ job?.title }}</div>
        <div class="pl-10 text-[#FF6400] text-2xl">{{ job?.salary }}元</div>
      </div>
      <div>
        <n-button
          class="mx-5"
          strong
          secondary
          type="tertiary"
          round
          @click="sendApplyApi(route.params.id)"
          >投简历</n-button
        >
      </div>
    </div>
    <div class="w-10/12 p-5">
      <n-row :gutter="30">
        <n-col :span="16" class="">
          <div class="bg-white shadow-md rounded p-5">
            <div class="text-xl">职位介绍</div>
            <n-space class="py-3">
              <n-tag :bordered="false" v-for="item in job.category?.split(',')">
                {{ item }}
              </n-tag>
            </n-space>
            <div class="whitespace-pre-wrap leading-5">
              {{ job?.description }}
            </div>
          </div>
          <div class="bg-white shadow-md rounded p-5 mt-7">
            <div class="flex">
              <n-input
                :placeholder="placeholder"
                v-model:value="content"
                ref="inputRef"
              />
              <n-button type="info" @click="handlePublish">发布</n-button>
            </div>
            <div class="py-5 text-lg">{{ job?.comments_count }}条评论</div>
            <div>
              <ChatItem
                v-for="item in job?.comments"
                :chat="item"
                @aaa="handleAAA"
                :class="{ 'pl-10': item.type == 2 }"
              />
            </div>
          </div>
        </n-col>
        <n-col :span="8">
          <div class="bg-white shadow-md rounded p-5 mb-3">
            <div class="text-xl pb-5">公司信息</div>
            <div class="flex">
              <n-avatar
                round
                :size="48"
                :src="BASE_URL + job?.company?.avatar"
              />
              <div class="flex flex-col pl-5 justify-center">
                <div class="py-2">
                  <n-text class="pr-2">{{ job?.company?.title }}</n-text>
                  <n-tag size="small" type="warning">已认证</n-tag>
                </div>
              </div>
            </div>
            <div class="aaa-item">
              <div>企业行业:{{ job?.company?.company_type }}</div>
              <div>企业资产:{{ job?.company?.captical }}</div>
              <div>人数规模:{{ job?.company?.staff_size }}</div>
              <div>职位地址:{{ job?.company?.address }}</div>
            </div>
          </div>
          <div class="bg-white shadow-md rounded p-5">
            <div class="text-xl pb-4">公司简介</div>
            <div class="leading-5 text-sm">
              {{ job?.company?.description }}
            </div>
          </div>
        </n-col>
      </n-row>
    </div>
  </div>
</template>

<script setup>
import { useRoute } from "vue-router";
import ChatItem from "@/components/home/ChatItem.vue";
import { ref, onMounted, watch } from "vue";
import { getJobInfoApi, publishCommentApi, sendApplyApi } from "@/api";
import { BASE_URL } from "@/config";

const route = useRoute();
const job = ref({});
const content = ref();
const inputRef = ref(null);
const placeholder = ref("写下你的评论...");
const commentID = ref("None");

function initData(id) {
  getJobInfoApi(id).then((res) => {
    job.value = res;
  });
}

watch(
  () => route.params.id,
  () => initData(route.params.id)
);

function handleAAA(name, id) {
  inputRef.value.focus();
  console.log(inputRef.value.placeholder);
  placeholder.value = `回复 @${name} `;
  commentID.value = id.id;
}

function handlePublish() {
  console.log(content.value);
  let params = {
    content: content.value,
    comment_id: commentID.value,
  };
  publishCommentApi(route.params.id, params).then((res) => {
    content.value = "";
    placeholder.value = "写下你的评论...";
    commentID.value = "None";
    initData(route.params.id);
  });
}

onMounted(() => initData(route.params.id));
</script>

<style lang="scss" scoped>
.aaa-item {
  > * {
    @apply py-2;
  }
}
</style>
