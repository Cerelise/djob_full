<template>
	<div class="w-full h-full pt-32 flex-col pl-32">
		<div class="text-4xl">发布工作</div>
		<div class="pt-5">
			<n-form class="w-5/12" ref="formRef" :model="form" :rules="JOB_RULES">
				<n-form-item label="工作名称" path="title">
					<n-input clearable v-model:value="form.title" />
				</n-form-item>
				<n-form-item label="工作地址" path="title">
					<n-input clearable v-model:value="form.location" />
				</n-form-item>
				<n-form-item label="类型" path="title">
					<n-select
						v-model:value="form.category"
						filterable
						multiple
						tag
						placeholder="输入，按回车确认"
						:show-arrow="false"
						:show="false"
					/>
				</n-form-item>
				<!-- <n-form-item label="招聘人数" path="title">
          <n-input clearable type="number" v-model:value="form.vacancy">
            <template #suffix> 人 </template>
          </n-input>
        </n-form-item> -->
				<n-form-item label="工资" path="title">
					<n-input clearable type="number" v-model:value="form.salary">
						<template #suffix> 元 </template>
					</n-input>
				</n-form-item>
				<n-form-item label="工作描述" path="title">
					<n-input
						clearable
						type="textarea"
						:rows="8"
						v-model:value="form.description"
					/>
				</n-form-item>
				<n-form-item>
					<n-button
						type="success"
						class="w-full"
						@click="publish"
						:loading="loading"
						>发布</n-button
					>
				</n-form-item>
			</n-form>
		</div>
	</div>
</template>

<script setup>
import { ref, reactive } from "vue";
import { createJobApi } from "@/api";
import { JOB_RULES } from "@/config";
import { resetForm } from "@/utils";
const form = reactive({});
const formRef = ref();
const loading = ref(false);
function publish() {
	formRef.value.validate((err) => {
		if (err) return;
		form.category = form.category.join(",");
		loading.value = true;
		createJobApi(form)
			.then((res) => {
				resetForm(form);
			})
			.finally(() => (loading.value = false));
	});
}
</script>

<style lang="scss" scoped></style>
