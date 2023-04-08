
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') },
      { path: 'newgame', component: () => import('pages/NewGamePage.vue') },
      { path: 'story', component: () => import('src/pages/StoryPage.vue') },
      { path: 'story/:id', component: () => import('src/pages/StoryPage.vue') }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
