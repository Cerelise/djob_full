<template>
  <div class="flex justify-between items-center px-20">
    <n-text>123</n-text>
    <div class="flex justify-center items-center">
      <n-badge
        :value="active"
        :max="99"
        class="mr-7"
        @click="$router.push('/admin/approval')"
      >
        <n-icon size="35"><EmailSharp /> </n-icon>
      </n-badge>
      <n-dropdown :options="options" @select="handleSelect">
        <span class="flex justify-center items-center">
          <n-avatar />
          <n-text class="pl-1">admin</n-text>
        </span>
      </n-dropdown>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { EmailSharp } from "@vicons/material";
import { getUserApplyApi } from "@/api";
import storage from "@/utils/storage";
import { removeToken } from "@/utils/auth";
import { toast } from "@/utils";
import { useRouter } from "vue-router";
const router = useRouter();
const active = ref(0);
const options = [
  {
    label: "用户资料",
    key: "profile",
  },
  {
    label: "退出登录",
    key: "logout",
  },
];
function handleSelect(e) {
  switch (e) {
    case "profile":
      router.push("/profile");
      break;
    case "logout":
      storage.clearAll();
      removeToken();
      toast("退出登录成功");
      router.push("/login");
      break;
  }
}
getUserApplyApi().then((res) => {
  console.log(res);
  active.value = res.length;
});
</script>

<style lang="scss" scoped></style>
