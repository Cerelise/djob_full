import { createApp } from 'vue'
import App from './App.vue'
import { router } from './router'
import Vue3Toastify from 'vue3-toastify';
import { createPinia } from 'pinia'

import "tailwindcss/tailwind.css"
import "./assets/css/reset.css"
import 'vue3-toastify/dist/index.css';


createApp(App).use(Vue3Toastify, {
  autoClose: 3000,
}).use(router).use(createPinia()).mount('#app')
