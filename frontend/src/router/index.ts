// Platform-v3\frontend\src\router\index.ts

import { createRouter, createWebHistory } from 'vue-router'
import CalculatorView from '../views/CalculatorView.vue'
import FertilizerListView from '../components/admin/FertilizerList.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'calculator',
      component: CalculatorView
    },
    {
      path: '/admin/fertilizers',
      name: 'fertilizers',
      component: FertilizerListView
    }
  ]
})

export default router