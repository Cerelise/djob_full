import { createRouter, createWebHistory } from 'vue-router';
import { getToken } from '@/utils/auth'
import { showFullLoading, hideFullLoading } from '@/utils'

import backend from '@/layout/Backend/index.vue'
import frontend from '@/layout/Frontend/index.vue'
import AdminHome from "@/views/admin/home.vue"
import Home from "@/views/home/home.vue"

const routes = [
  {
    path: "/",
    component: frontend,
    redirect: "/home",
    children: [
      {
        path: "/home",
        component: Home,
        meta: {
          title: "主页"
        }
      },
      {
        path: "/search-jobs",
        component: () => import("@/views/home/SearchJobs.vue"),
        meta: {
          title: "找工作"
        }
      },
      {
        path: "/my-jobs",
        component: () => import("@/views/home/MyJobs.vue"),
        meta: {
          title: "添加工作"
        }
      },
      {
        path: "/job-info/:id",
        component: () => import("@/views/home/JobInfo.vue"),
        meta: {
          title: "工作详情"
        }
      },
      {
        path: "/profile",
        component: () => import("@/views/home/profile.vue"),
        meta: {
          title: "个人信息"
        }
      },
      {
        path: "/deal-with-the-work",
        component: () => import("@/views/home/DealWork.vue"),
        meta: {
          title: "处理工作"
        }
      },
      {
        path: "/publish-work",
        component: () => import("@/views/home/PublishWork.vue"),
        meta: {
          title: "发布工作"
        }
      },
    ]

  },
  {
    path: "/admin",
    component: backend,
    redirect: "/admin/home",
    children: [
      {
        path: "/admin/home",
        component: AdminHome,
        meta: {
          title: "用户管理"
        }
      },
      {
        path: "/admin/comment",
        component: () => import("@/views/admin/comment.vue"),
        meta: {
          title: "评论管理"
        }
      },
      {
        path: "/admin/approval",
        component: () => import("@/views/admin/approval.vue"),
        meta: {
          title: "审批管理"
        }
      },
    ]
  },

  { path: '/login', component: () => import("@/views/user/login.vue") },
  { path: '/signup', component: () => import("@/views/user/signup.vue") },
  { path: '/:pathMatch(.*)', component: () => import("@/views/other/404.vue") }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from) => {
  console.log(to.path)
  const token = getToken()
  // if (to.path == "/login" && token) return "/home"

  showFullLoading()
})
router.afterEach((to, from) => hideFullLoading())
export { router }