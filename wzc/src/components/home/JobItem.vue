<template>
  <div
    class="flex justify-between items-center py-5 px-10 shadow-xl border border-solid border-gray-100 my-10"
    @click.stop="$router.push(`/job-info/${item.id}`)"
  >
    <n-space vertical size="medium">
      <div class="text-xl font-medium">{{ item.title }}</div>
      <n-rate size="large" readonly :default-value="item.vacancy" />
      <n-text>工资:{{ item.salary }}</n-text>
      <n-text>公司地址:{{ item.location }}</n-text>
      <n-space>
        <n-tag
          v-for="i in item.category?.split(',')"
          type="success"
          size="small"
          round
        >
          {{ i }}
        </n-tag>
      </n-space>
    </n-space>
    <n-image
      width="100"
      src="https://07akioni.oss-cn-beijing.aliyuncs.com/07akioni.jpeg"
    />
  </div>
  <n-modal
    v-model:show="showModal"
    preset="card"
    title="编辑工作"
    size="huge"
    :bordered="false"
    class="w-96"
  >
    {{ item.title }}
  </n-modal>
</template>

<script setup>
import { ref } from "vue";
const showModal = ref(false);
const { item } = defineProps({
  item: {
    type: Object,
    default: () => ({
      title: "SOftWare Development Intern",
      rate: 3,
      salary: "Salary:Internship",
      duration: ":Internship",
      posted: "Internship",
      location: "Internship",
      category: '"c", "C++", "JAVA", "PHP"',
      id: 123123123123,
    }),
  },
});
function handlePositiveClick() {
  console.log(item);
}
</script>

<style lang="scss" scoped></style>
