<template>
	<div
		class="my-2 p-3 flex justify-between items-center hover:bg-[#F3F3F5] cursor-default"
	>
		<div class="flex items-center">
			<n-avatar :size="70" round :src="BASE_URL + item?.created_by?.avatar" />
			<div class="flex justify-center items-center flex-col px-5">
				<n-text>{{ item.created_by?.name }}</n-text>
			</div>

			<n-text class="pr-5">申请了 {{ item.job.title }}的工作</n-text>
			<a
				:href="BASE_URL + item?.created_by?.resume"
				target="_blank"
				class="hover:underline"
				>查看简历</a
			>
		</div>
		<!-- 默认值：处理中 -->
		<div v-if="item.status == '处理中' && user?.is_employer">
			<n-button type="success" @click="pass(item.id, '通过')">通过</n-button>
			<n-button type="error" class="ml-5" @click="pass(item.id, '驳回')"
				>驳回</n-button
			>
		</div>
		<div v-else>
			<n-tag :type="jobStatus">{{ item.status }}</n-tag>
		</div>
	</div>
</template>

<script setup>
import { BASE_URL } from "@/config";
import { passUserApplyApi } from "@/api";
import { computed } from "vue";
import storage from "@/utils/storage";

const { item } = defineProps({
	item: Object,
});

const user = storage.getItem("user");

const jobStatus = computed(() => {
	if (item) {
		if (item.status == "处理中") return "warning";
		else if (item.status == "驳回") return "error";
		else return "success";
	}
});

const emit = defineEmits(["reload"]);
function pass(id, status) {
	passUserApplyApi(id, status).then((res) => {
		emit("reload");
	});
}
</script>

<style lang="scss" scoped></style>
