import { createRouter, createWebHistory } from 'vue-router';

import main from '@/views/main_page.vue';
import serviceIntroduce from '@/views/service_introduce_page.vue';
import newsCliping from '@/views/news_cliping_page.vue';
import checkList from '@/views/check_list_page.vue';
import loading from '@/views/loading_page.vue';
import preview from '@/views/preview_page.vue';

const routes = [
  {
    path: '/',
    name: 'main',
    component: main,
  },
  {
    path: '/serviceIntroduce',
    name: 'serviceIntroduce',
    component: serviceIntroduce,
  },
  {
    path: '/newsCliping',
    name: 'newsCliping',
    component: newsCliping,
  },
  {
    path: '/checkList',
    name: 'checkList',
    component: checkList,
  },
  {
    path: '/loading',
    name: 'loading',
    component: loading,
  },
  {
    path: '/preview',
    name: 'preview',
    component: preview,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;