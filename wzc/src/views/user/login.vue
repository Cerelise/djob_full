<template>
  <div class="w-full h-[100vh] flex items-center justify-center">
    <div class="w-96 h-80 shadow-md flex justify-center items-center flex-col">
      <div class="text-3xl font-bold pb-5">Login</div>
      <n-form
        ref="formRef"
        label-width="auto"
        label-placement="left"
        :model="form"
        :rules="RULES"
        class="w-10/12"
      >
        <n-form-item path="email">
          <n-input
            v-model:value="form.email"
            placeholder="请输入用户名"
            clearable
          />
        </n-form-item>
        <n-form-item path="password">
          <n-input
            placeholder="请输入密码"
            type="password"
            clearable
            v-model:value="form.password"
            show-password-on="click"
          />
        </n-form-item>
        <n-form-item>
          <n-button @click="login" :loading="loading" type="info" class="w-full"
            >登录</n-button
          >
        </n-form-item>
      </n-form>
      <div
        @click="$router.push('/signup')"
        class="text-sm hover:underline cursor-pointer text-[#A7A7A7]"
      >
        还没有账号？点击注册
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from "vue";

import { RULES } from "@/config";
import { setToken } from "@/utils/auth";
import { loginApi } from "@/api";
import { useRouter } from "vue-router";
import storage from "@/utils/storage";

const form = reactive({});
const loading = ref(false);
const formRef = ref(null);
const router = useRouter();
function login() {
  formRef.value.validate((err) => {
    if (err) return;
    loading.value = true;
    loginApi(form)
      .then((res) => {
        setToken(res.token ? res.token : null);
        storage.setItem("user", res.user);
        if (res.user?.is_admin) router.push("/admin");
        else router.push("/home");
      })
      .finally(() => (loading.value = false));
  });
}
</script>

<style lang="scss" scoped></style>
