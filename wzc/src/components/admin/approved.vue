<template>
	<n-empty v-if="data.length == 0" />
	<n-collapse accordion v-else>
		<n-collapse-item
			:title="item.title"
			:name="item.id"
			v-for="item in companyData"
			class="cursor-default"
		>
			<div>企业行业: {{ item.company_type }}</div>
			<div>企业资产: {{ item.captical }}</div>
			<div>人数规模: {{ item.staff_size }}</div>
			<div>企业地址: {{ item.address }}</div>
			<div>经营范围: {{ item.business_scope }}</div>
			<div>工作描述: {{ item.description }}</div>
			<div>发布时间: {{ item.created_at }}</div>
			<template #header-extra>
				<n-tag type="success" v-if="item.status == 1"> 已通过 </n-tag>
				<n-tag type="error" v-else> 已打回 </n-tag>
			</template>
		</n-collapse-item>

		<n-collapse-item
			:title="item.title"
			:name="item.id"
			v-for="item in jobData"
			class="cursor-default"
		>
			<div>工作分类: {{ item.category }}</div>
			<div>发布公司: {{ item.company_name }}</div>
			<div>公司地址: {{ item.location }}</div>
			<div>工作描述: {{ item.description }}</div>
			<div>发布时间: {{ item.created_at }}</div>
			<template #header-extra>
				<n-tag type="success" v-if="item.status == 1"> 已通过 </n-tag>
				<n-tag type="error" v-else> 已打回 </n-tag>
			</template>
		</n-collapse-item>
	</n-collapse>
</template>

<script setup>
import { getApprovalsApi } from "@/api";
import { ref, onMounted } from "vue";

const data = ref([]);
const jobData = ref([]);
const companyData = ref([]);
function getData() {
	getApprovalsApi("all").then((res) => {
		data.value = res;
		for (let i = 0; i < data.value.length; i++) {
			let item = data.value[i];
			if (item.location) {
				jobData.value.push(item);
			} else if (item.address) {
				companyData.value.push(item);
			}
		}
		// console.log(`job：${JSON.stringify(jobData.value)}`);
		// console.log(`company：${companyData.value}`);
	});
}
onMounted(() => getData());
</script>

<style lang="scss" scoped></style>
