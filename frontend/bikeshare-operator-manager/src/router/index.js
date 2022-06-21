import Vue from 'vue'
import VueRouter from 'vue-router'
import login from '../components/Login/Login.vue'
import home from '../components/Operator/home.vue'
import welcome from '../components/Operator/welcome.vue'
import bikeMap from '../components/Operator/bike/bikeMap.vue'
import bikeSearch from '../components/Operator/bike/bikeSearch.vue'
import repairOrder from '../components/Operator/repair/repairOrder.vue'
import repairRequest from '../components/Operator/repair/repairRequest.vue'
import moveOrder from '../components/Operator/transport/moveOrder.vue'
import locationNumber from '../components/Operator/transport/locationNumber.vue'
import editInfo from '../components/Operator/editInfo.vue'
import bikeRegister from '../components/Operator/bike/bikeRegister.vue'

import database from '../components/Manager/Database.vue'

Vue.use(VueRouter)


const routes = [{
    path: '/',
    component: login
  },
  {
    path: '/login',
    component: login
  },
  {
    path: '/operator',
    component: home,
    redirect: '/welcome',
    children: [{
        path: '/welcome',
        component: welcome
      },
      {
        path: '/bikeMap',
        component: bikeMap
      },
      {
        path: '/bikeSearch',
        component: bikeSearch
      },
      {
        path: '/bikeRegister',
        component: bikeRegister
      },
      {
        path: '/moveOrder',
        component: moveOrder
      },
      {
        path: '/locationNumber',
        component: locationNumber
      },
      {
        path: '/repairRequest',
        component: repairRequest
      },
      {
        path: '/repairOrder',
        component: repairOrder
      },
      {
        path: '/editInfo',
        component: editInfo
      }
    ]
  },
  {
    path: '/manager',
    component: database
  }
]

const router = new VueRouter({
  routes
})

export default router
