<template>
  <div
    class="flex mb-5 hover:bg-[#F3F3F5] p-3 border-b border-solid border-[#F3F3F5]"
  >
    <n-avatar :src="BASE_URL + chat?.created_by?.avatar" />
    <div class="flex justify-between items-end w-full pl-2">
      <div>
        <div>{{ chat?.created_by?.name }}</div>
        <div class="py-2">{{ chat?.content }}</div>
        <div class="text-sm text-[#9196A1]">
          {{ chat?.created_at?.split(" ")[0] }}
        </div>
      </div>
      <div
        v-if="!show"
        class="flex justify-center items-center cursor-pointer"
        @click="$emit('aaa', chat?.created_by?.name, chat)"
      >
        <n-icon color="#8491A5" size="20"><ChatBubbleFilled /></n-icon>
        <div class="pl-1">回复</div>
      </div>
    </div>
  </div>
  <div class="ml-14">
    <ChatItem v-for="item in chat.comment_replied" :chat="item" show />
  </div>
</template>

<script setup>
import { ChatBubbleFilled } from "@vicons/material";
import { BASE_URL } from "@/config";
const { chat } = defineProps({
  chat: Object,
  show: {
    type: Boolean,
    default: false,
  },
});

setTimeout(() => console.log(chat), 5000);
</script>

<style lang="scss" scoped></style>
