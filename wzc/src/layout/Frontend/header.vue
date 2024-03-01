<template>
	<div
		class="fixed top-0 h-14 w-full bg-[#3852AE] flex justify-between items-center px-8 text-white z-50"
	>
		<div class="cursor-pointer text-xl" @click="$router.push('/home')">
			Job Portal
		</div>
		<div class="flex items-center items-center cursor-pointer">
			<div v-for="item in menu" class="p-3" @click="$router.push(item.path)">
				<span>{{ item.title }}</span>
			</div>
			<n-dropdown :options="profile" @select="handleDropdown">
				<div>个人资料</div>
			</n-dropdown>
		</div>
	</div>
</template>

<script setup>
import { ref, computed } from "vue";
import storage from "@/utils/storage";
import { removeToken } from "@/utils/auth";
import { toast } from "@/utils";
import { useRouter } from "vue-router";
const router = useRouter();
const user = ref(storage.getItem("user"));
const menus = [
	{
		title: "找工作",
		path: "/search-jobs",
		role: [0, 1],
	},
	{
		title: "我的工作申请",
		path: "/my-jobs",
		role: [1],
	},
	{
		title: "处理工作申请",
		path: "/deal-with-the-work",
		role: [0],
	},
	{
		title: "发布工作",
		path: "/publish-work",
		role: [0],
	},
];

const menu = computed(() =>
	menus.filter((el) => el.role.includes(user?.value?.is_employer ? 0 : 1))
);
const profile = [
	{
		label: "个人信息",
		key: "/profile",
	},
	{
		label: "退出登录",
		key: "logout",
	},
	{
		label: "后台管理",
		key: "/admin",
		show: user.value?.is_admin,
	},
];
function handleDropdown(e) {
	console.log(e);
	if (e == "logout") {
		storage.clearAll();
		removeToken();
		toast("退出登录成功");
		router.push("/login");
	} else router.push(e);
}
</script>

<style lang="scss" scoped></style>
