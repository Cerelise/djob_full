<template>
  <n-result
    status="404"
    title="404 资源不存在"
    :description="num + '秒后跳转回主页'"
    class="pt-24"
  >
    <template #footer>
      <n-button @click="router.push('/home')">点击返回主页</n-button>
    </template>
  </n-result>
</template>

<script setup>
import { useRouter } from "vue-router";
import { onMounted, ref } from "vue";
const num = ref(5);
const router = useRouter();
onMounted(() => {
  setTimeout(() => {
    router.push("/home"); // Replace '/new-page' with the actual route you want to redirect to
  }, 5000);

  setInterval(() => {
    num.value -= 1;
  }, 1000);
});
</script>
