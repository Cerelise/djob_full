<template>
  <n-card>
    <n-tabs type="line" animated>
      <n-tab-pane name="审批公司" tab="审批公司">
        <ApprovalCompVue />
      </n-tab-pane>
      <n-tab-pane name="审批工作" tab="审批工作">
        <ApprovalJobVue />
      </n-tab-pane>
      <n-tab-pane name="已审批" tab="已审批"> <approved /> </n-tab-pane>
    </n-tabs>
  </n-card>
</template>

<script setup>
import ApprovalCompVue from "@/components/admin/ApprovalComp.vue";
import ApprovalJobVue from "@/components/admin/ApprovalJob.vue";
import approved from "@/components/admin/approved.vue";
</script>

<style lang="scss" scoped></style>
