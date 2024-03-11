<template>
	<div class="w-full h-[100vh] flex items-center justify-center">
		<div
			class="w-96 h-[30rem] shadow-md flex justify-center items-center flex-col"
		>
			<div class="text-3xl font-bold pb-3">Signup</div>
			<n-form
				ref="formRef"
				label-width="auto"
				label-placement="left"
				:model="form"
				:rules="RULES"
				class="w-10/12"
			>
				<n-form-item path="email">
					<n-input v-model:value="form.email" placeholder="请输入邮箱地址" />
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
				<n-form-item path="reenteredPassword">
					<n-input
						placeholder="请确认密码"
						type="password"
						clearable
						v-model:value="form.reenteredPassword"
						show-password-on="click"
					/>
				</n-form-item>
				<n-form-item path="email">
					<div class="flex w-full gap-2">
						<n-input v-model:value="form.code" placeholder="请输入验证码" />
						<n-button :disabled="show" type="info" @click="getCode">
							{{ show ? countdown : "获取验证码" }}</n-button
						>
					</div>
				</n-form-item>
				<!-- <n-form-item path="code">
					<n-input v-model:value="form.code" placeholder="请输入验证码" />
				</n-form-item> -->
				<n-form-item>
					<n-switch v-model:value="form.is_employer">
						<template #checked> 企业用户 </template>
						<template #unchecked> 普通用户 </template>
					</n-switch>
				</n-form-item>
				<n-form-item>
					<n-button
						@click="register"
						:loading="loading"
						type="info"
						class="w-full"
						>注册</n-button
					>
				</n-form-item>
			</n-form>
			<div
				@click="$router.push('/login')"
				class="text-sm hover:underline cursor-pointer text-[#A7A7A7]"
			>
				已有账号？点击登录
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, reactive, computed } from "vue";
import { RULES } from "@/config";
import { toast } from "@/utils";
import { registerApi, sendVerifyEmail } from "@/api";
import { useRouter } from "vue-router";

const form = reactive({
	username: "",
	is_employer: false,
});
const loading = ref(false);
const formRef = ref(null);
const router = useRouter();
const countdown = ref(60);
const show = computed(() => countdown.value > 0 && countdown.value < 60);
function register() {
	formRef.value.validate((err) => {
		if (err) return;
		loading.value = true;
		registerApi(form)
			.then((res) => {
				setTimeout(() => {
					router.push("/login");
				}, 1000);
			})
			.finally(() => (loading.value = false));
	});
}
function getCode() {
	if (
		!/^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/.test(form.email)
	)
		return toast("请先输入正确的邮箱格式在获取验证码", "error");

	sendVerifyEmail({ email: form.email }).then((res) => {
		countdown.value--;
		let timer;
		timer = setInterval(() => {
			countdown.value--;
			if (countdown.value <= 0) clearInterval(timer);
		}, 1000);
	});
}
</script>

<style lang="scss" scoped></style>
