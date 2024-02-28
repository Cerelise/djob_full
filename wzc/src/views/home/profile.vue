<template>
  <div class="my-10 px-32">
    <n-row :gutter="30">
      <n-col :span="16">
        <div class="flex items-center">
          <n-avatar :size="75" round :src="BASE_URL + userinfo.avatar" />
          <n-space vertical class="pl-3">
            <n-text>姓名:{{ userinfo.name }}</n-text>
            <n-text>邮箱:{{ userinfo.email }}</n-text>
            <n-text>用户性别:{{ userinfo.gender }}</n-text>
            <n-text
              >用户身份:
              <n-tag type="success">{{
                userinfo.is_employer ? "招聘者" : "普通用户"
              }}</n-tag>
            </n-text>
            <n-text>注册时间:{{ userinfo.date_joined }}</n-text>
          </n-space>
          <n-button type="success" class="ml-5" @click="showEditProfile = true"
            >编辑个人信息</n-button
          >
        </div>
        <div>
          <div class="text-2xl py-5 pt-32">我的消息</div>
          <n-list hoverable clickable>
            <n-list-item
              v-for="item in messages"
              @click="deal_word(item.notification_status)"
            >
              <div class="flex items-center">
                <n-avatar
                  :size="75"
                  round
                  :src="BASE_URL + item.created_by.avatar"
                />
                <div class="px-5">
                  <div>
                    <span class="text-2xl font-bold">{{
                      item.created_by.name
                    }}</span>
                    给你发送了通知
                  </div>
                  <div class="text-xl">{{ item.content }}</div>

                  <div class="text-[#797979] text-sm">
                    {{ item.created_at?.split("T")[0] }}
                  </div>
                </div>
                <n-tag type="success" v-if="item.notification_status == 1"
                  >通过</n-tag
                >
                <n-tag type="warning" v-else-if="item.notification_status == 0"
                  >处理中</n-tag
                >
                <n-tag type="error" v-else>驳回</n-tag>
              </div>
            </n-list-item>
          </n-list>
        </div>
      </n-col>
      <n-col :span="8" v-if="userinfo.is_employer">
        <n-empty description="您还没有所属公司" class="pt-20" v-if="!company">
          <template #extra>
            <n-button size="small" type="success" @click="showModal = true">
              加入公司
            </n-button>
          </template>
        </n-empty>
        <div v-else>
          <div class="bg-white shadow-md rounded p-5">
            <div class="text-xl pb-4">公司信息</div>
            <div class="flex">
              <n-avatar round :size="48" :src="BASE_URL + company?.avatar" />
              <div class="flex flex-col pl-5 justify-center">
                <div class="py-2">
                  <n-text class="pr-2">{{ company?.title }}</n-text>
                  <n-tag size="small" type="warning">已认证</n-tag>
                </div>
              </div>
            </div>
            <div class="aaa-item">
              <div>企业行业:{{ company?.company_type }}</div>
              <div>企业资产:{{ company?.captical }}</div>
              <div>人数规模:{{ company?.staff_size }}</div>
              <div>公司地址:{{ company?.address }}</div>
              <div>经营范围:{{ company?.business_scope }}</div>
            </div>
            <div class="leading-5 text-sm">
              {{ company?.description }}
            </div>
          </div>
        </div>
      </n-col>
      <n-col :span="8" v-else>
        <div class="text-2xl">个人简历</div>
        <n-empty description="可以点击下方查看简历以查看" class="pt-20">
          <template #extra>
            <a
              v-if="userinfo.resume"
              :href="BASE_URL + userinfo.resume"
              target="_blank"
              >查看简历</a
            >
            <n-upload
              class="pt-10"
              :action="BASE_URL + 'api/auth/user/resume'"
              :headers="{
                Authorization: 'Bearer ' + getToken(),
              }"
              name="resume"
              accept=".pdf"
              :show-file-list="false"
              @before-upload="beforeUpload"
              @finish="handleFinish"
            >
              <n-button>上传简历</n-button>
            </n-upload>
          </template>
        </n-empty>
      </n-col>
    </n-row>

    <n-modal
      v-model:show="showModal"
      preset="card"
      :mask-closable="false"
      title="创建公司"
      :bordered="false"
      class="w-[35rem]"
    >
      <n-form
        label-width="auto"
        label-placement="left"
        label-align="right"
        ref="formRef"
        :model="form"
        :rules="COMP_RULES"
      >
        <n-form-item label="公司logo">
          <n-upload
            list-type="image-card"
            :max="1"
            accept=".png,jpg,.jpeg"
            :default-upload="false"
            @change="handleChange"
          >
            点击上传
          </n-upload>
        </n-form-item>
        <n-form-item label="公司名称" path="title">
          <n-input clearable v-model:value="form.title" />
        </n-form-item>
        <n-form-item label="公司地址" path="address">
          <n-input clearable v-model:value="form.address" />
        </n-form-item>
        <n-form-item label="公司行业" path="address">
          <n-input clearable v-model:value="form.company_type" />
        </n-form-item>
        <n-form-item label="公司规模" path="address">
          <n-input clearable type="number" v-model:value="form.staff_size">
            <template #suffix> 人 </template>
          </n-input>
        </n-form-item>
        <n-form-item label="注册资本" path="address">
          <n-input clearable type="number" v-model:value="form.captical">
            <template #suffix> 元 </template>
          </n-input>
        </n-form-item>
        <n-form-item label="经营范围" path="address">
          <n-input
            clearable
            type="textarea"
            :rows="3"
            v-model:value="form.business_scope"
          />
        </n-form-item>
        <n-form-item label="公司描述" path="address">
          <n-input
            clearable
            type="textarea"
            :rows="7"
            v-model:value="form.description"
          />
        </n-form-item>
        <n-form-item>
          <n-button type="success" class="w-full" @click="addCompany"
            >保存</n-button
          >
        </n-form-item>
      </n-form>
    </n-modal>
    <n-modal
      v-model:show="showEditProfile"
      preset="card"
      :mask-closable="false"
      title="编辑个人信息"
      :bordered="false"
      class="w-96"
    >
      <n-form
        label-width="auto"
        label-placement="left"
        label-align="right"
        :model="profile"
        :rules="rules"
      >
        <n-form-item label="用户头像">
          <n-upload
            :action="BASE_URL + 'api/auth/user/avatar'"
            :default-file-list="fileList"
            list-type="image-card"
            :headers="{
              Authorization: 'Bearer ' + getToken(),
            }"
            :max="1"
            accept=".png,jpg,.jpeg"
            name="avatar"
            @finish="handleFinish"
          >
            点击上传
          </n-upload>
        </n-form-item>
        <n-form-item label="用户用户">
          <n-input v-model:value="profile.name" clearable />
        </n-form-item>
        <n-form-item label="用户性别">
          <n-select v-model:value="profile.gender" :options="sex" />
        </n-form-item>
        <n-form-item label="手机号码">
          <n-input v-model:value="profile.phone" clearable />
        </n-form-item>
        <n-form-item label="描述">
          <n-input
            v-model:value="profile.description"
            clearable
            type="textarea"
            :rows="5"
          />
        </n-form-item>
        <n-form-item>
          <n-button type="success" class="w-full" @click="editUser"
            >保存</n-button
          >
        </n-form-item>
      </n-form>
    </n-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import storage from "@/utils/storage";
import { BASE_URL, COMP_RULES } from "@/config";
import { getToken } from "@/utils/auth";
import { toast, resetForm } from "@/utils";
import {
  getUserinfoApi,
  getUserApplyApi,
  editUserinfoApi,
  createCompApi,
  uploadCompLogoApi,
  getCompInfoApi,
} from "@/api";
import { useRouter } from "vue-router";

const router = useRouter();
const company = ref(null);
const showModal = ref(false);
const showEditProfile = ref(false);
const formRef = ref();
const form = reactive({});
const rules = [];
const userinfo = ref(storage.getItem("user"));
const profile = reactive(userinfo.value);
const messages = ref();
const sex = [
  {
    label: "男",
    value: "男",
  },
  {
    label: "女",
    value: "女",
  },
  {
    label: "未知",
    value: "未知",
  },
];
const fileList = ref([
  {
    id: "a",
    url: BASE_URL + userinfo.value.avatar,
    status: "finished",
  },
]);

function editUser() {
  editUserinfoApi(profile).then((res) => {
    showEditProfile.value = false;
    resetForm(profile);
    getUserinfoApi().then((res) => {
      userinfo.value = res;
      storage.setItem("user", res);
    });
  });
}
function addCompany() {
  formRef.value.validate((err) => {
    if (err) return;
    if (!form.logo) return toast("请先上传头像", "error");
    createCompApi(form).then((res) => {
      console.log(res);
      showModal.value = false;
    });
  });
}
function handleChange(e) {
  console.log(e);
  const formData = new FormData();
  const file = e.file;
  console.log(file);
  formData.append("logo", file.file, file.name);
  uploadCompLogoApi(formData).then((res) => {
    form.logo = res;
  });
}

function beforeUpload(data) {
  console.log(data.file.file?.type);
  if (data.file.file?.type !== "application/pdf") {
    toast("只能上传pdf文件，请重新上传", "error");
    return false;
  }
  return true;
}
function deal_word(key) {
  if (key == 0) router.push("/deal-with-the-work");
}
function handleFinish(e) {
  toast("文件上传成功");
  getUserinfoApi().then((res) => {
    userinfo.value = res;
    storage.setItem("user", res);
  });
}

onMounted(() => {
  getUserApplyApi().then((res) => {
    console.log(res);
    messages.value = res;
  });
  getCompInfoApi(userinfo.value.id).then((res) => (company.value = res));
});
</script>

<style lang="scss" scoped>
.aaa-item {
  > * {
    @apply py-2;
  }
}
</style>
