<template>
  <div class="w-full m-3">
    <n-card class="mb-3">
      <n-form :model="searchKey" inline label-placement="left">
        <n-form-item label="用户姓名">
          <n-input v-model:value="searchKey.name" />
        </n-form-item>
        <n-form-item label="用户类型">
          <n-select
            class="w-60"
            v-model:value="searchKey.type"
            :options="options"
            clearable
          />
        </n-form-item>
        <n-form-item>
          <n-button type="success" @click="getData()">搜索</n-button>
          <n-button type="info" class="ml-3" @click="reset">重置</n-button>
        </n-form-item>
      </n-form>
    </n-card>
    <n-card>
      <n-button type="success" class="m-1" @click="showModal = true">
        新增用户
      </n-button>
      <n-table :bordered="false" :single-line="false" class="my-5">
        <thead>
          <tr>
            <th>头像</th>
            <th>姓名</th>
            <th>邮箱</th>
            <th>性别</th>
            <th>手机号</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in data">
            <td>
              <n-avatar size="large" :src="BASE_URL + item.avatar" />
            </td>
            <td>{{ item.name }}</td>
            <td>{{ item.email }}</td>
            <td>{{ item.gender }}</td>
            <td>{{ item.phone }}</td>
            <td>
              <n-popconfirm @positive-click="handleDelete(item.id)">
                <template #trigger>
                  <n-button type="error" class="ml-3">删除</n-button>
                </template>
                确定要删除吗
              </n-popconfirm>
            </td>
          </tr>
        </tbody>
      </n-table>
      <div class="w-full flex justify-center">
        <n-pagination
          v-model:page="page"
          :page-count="count"
          :on-update:page="handleUpdate"
        />
      </div>
      <n-modal
        v-model:show="showModal"
        :mask-closable="false"
        preset="card"
        title="操作用户"
        class="w-[30rem]"
      >
        <n-form
          ref="formRef"
          label-width="auto"
          label-placement="left"
          :model="form"
          :rules="RULES"
        >
          <n-form-item path="email" label="用户邮箱">
            <n-input
              v-model:value="form.email"
              placeholder="请输入用户名"
              clearable
            />
          </n-form-item>
          <n-form-item path="password" label="用户密码">
            <n-input
              placeholder="请输入密码"
              clearable
              v-model:value="form.password"
            />
          </n-form-item>
          <n-form-item label="用户身份">
            <n-switch v-model:value="form.is_employer">
              <template #checked> 企业用户 </template>
              <template #unchecked> 普通用户 </template>
            </n-switch>
          </n-form-item>
          <n-form-item>
            <n-button
              class="w-full"
              type="success"
              @click="createUser"
              :loading="loading"
              >创建</n-button
            >
          </n-form-item>
        </n-form>
      </n-modal>
    </n-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import { getUsersApi, createUserApi, deleteUserApi } from "@/api";
import { BASE_URL } from "@/config";
import { resetForm } from "@/utils";

const showModal = ref(false);
const loading = ref(false);
const searchKey = reactive({});

const form = reactive({
  is_employer: false,
});
const formRef = ref();
const pagenum = ref(1);
const count = ref(0);
const data = ref();
import { RULES } from "@/config";

const options = [
  {
    label: "普通用户",
    value: "user",
  },
  {
    label: "企业用户",
    value: "employer",
  },
];
function getData() {
  let params = { page: pagenum.value, ...searchKey };
  getUsersApi(params).then((res) => {
    if (res?.count && res?.data) {
      count.value = Math.ceil(res.count / 6);
      data.value = res.data;
    } else data.value = [];
  });
}

function reset() {
  resetForm(searchKey);
  getData();
}
function createUser() {
  formRef.value.validate((err) => {
    if (err) return;
    loading.value = true;
    createUserApi(form)
      .then((res) => {
        getData();
        resetForm(form);
        showModal.value = false;
      })
      .finally(() => (loading.value = false));
  });
}

function handleDelete(id) {
  deleteUserApi(id).then(() => getData());
}
function handleUpdate(page) {
  pagenum.value = page;
  getData();
}
onMounted(() => {
  getData();
});
</script>

<style lang="scss" scoped></style>
