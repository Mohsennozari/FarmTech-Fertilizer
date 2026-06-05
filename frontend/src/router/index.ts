// Platform-v3\frontend\src\router\index.ts

import { createRouter, createWebHistory } from 'vue-router'
import CalculatorView from '../views/CalculatorView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'calculator',
      component: CalculatorView
    }
  ]
})

export default router