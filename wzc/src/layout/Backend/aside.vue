<template>
  <n-layout-sider
    bordered
    collapse-mode="width"
    :collapsed-width="64"
    :width="240"
    :collapsed="collapsed"
    show-trigger
    @collapse="collapsed = true"
    @expand="collapsed = false"
  >
    <n-menu
      :collapsed="collapsed"
      :collapsed-width="64"
      :collapsed-icon-size="22"
      :options="menuOptions"
      :default-value="active"
    />
  </n-layout-sider>
</template>

<script setup>
import { h, ref, computed } from "vue";
import { NIcon } from "naive-ui";
import {
  SupervisedUserCircleOutlined,
  EditNoteFilled,
  ApprovalFilled,
} from "@vicons/material";
import { RouterLink, useRoute } from "vue-router";
const route = useRoute();
const active = computed(
  () => route.path.split("/")[route.path.split("/").length - 1]
);
const menuOptions = [
  {
    label: () =>
      h(
        RouterLink,
        { to: { path: "/admin/home" } },
        { default: () => "用户管理" }
      ),
    key: "home",
    icon: renderIcon(SupervisedUserCircleOutlined),
    show: true,
  },

  {
    label: () =>
      h(
        RouterLink,
        { to: { path: "/admin/comment" } },
        { default: () => "评论管理" }
      ),
    key: "comment",
    icon: renderIcon(EditNoteFilled),
  },
  {
    label: () =>
      h(
        RouterLink,
        { to: { path: "/admin/approval" } },
        { default: () => "审批管理" }
      ),
    key: "approval",
    icon: renderIcon(ApprovalFilled),
  },
];

const collapsed = ref(false);
function renderIcon(icon) {
  return () => h(NIcon, null, { default: () => h(icon) });
}
</script>

<style lang="scss" scoped></style>
