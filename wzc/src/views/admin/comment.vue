<template>
  <n-table :bordered="false" :single-line="false">
    <thead>
      <tr>
        <th>评论者头像</th>
        <th>评论者名字</th>
        <th>评论内容</th>
        <th>评论时间</th>
        <th>评论类型</th>
        <th>操作</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="item in data">
        <td>
          <n-avatar size="large" :src="BASE_URL + item.created_by?.avatar" />
        </td>
        <td>{{ item.created_by?.name }}</td>
        <td>{{ item.content }}</td>
        <td>{{ item.created_at }}</td>
        <td>{{ item.type_of == 1 ? "评论" : "回复" }}</td>
        <td>
          <n-popconfirm @positive-click="handleDelete(item.id, item.type_of)">
            <template #trigger>
              <n-button type="error" class="ml-3">删除</n-button>
            </template>
            确定要删除吗
          </n-popconfirm>
        </td>
      </tr>
    </tbody>
  </n-table>
</template>

<script setup>
import { getComments, deleteCommentApi } from "@/api";
import { ref, onMounted } from "vue";
import { BASE_URL } from "@/config";
const data = ref([]);
function handleDelete(id, type) {
  deleteCommentApi({ id, type: type + "" }).then(() => getData());
}
function getData() {
  getComments().then((res) => {
    console.log(res);
    data.value = res;
  });
}
onMounted(() => {
  getData();
});
</script>

<style lang="scss" scoped></style>
