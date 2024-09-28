import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import song_create from '../views/Song.vue'
import login from '../views/login.vue'
import album_create from '../views/Album_Creation.vue'
import playlist_create from '../views/Playlist_Creation.vue'
import user_data from '../views/page_user.vue'
import page_creator from '../views/page_creator.vue'
import song_view from '../views/Song_View.vue'
import song_edit from '../views/song_edit.vue'
import album_edit from '../views/album_edit.vue'
import admin_support from '../views/admin_support.vue'
import admin_dashboard from '../views/admin_dashboard.vue'
import admin_login from '../views/admin_login.vue'
import search from '../views/search.vue'
import Register from '@/views/Register.vue'
import forgotpass from '../views/forgotpass.vue'
import albply from '../views/albply_view.vue'
import policy from '../views/policy.vue'
import Audio from '../views/audiogen.vue'


const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  { 
    path: '/song/create',
    name: 'Song_Creation',
    component: song_create,
    meta: { requiresCreator: true }
  },  
  { 
    path: '/policy',
    name: 'policy',
    component: policy    
  },
  {
    path: '/song/:song_id/:value/add',
    name: 'Song_View',
    component: song_view,
    props: true
  },
  {
    path: '/user/:id/:code/edit_album',
    name: 'album_edit',
    component: album_edit,
    props: true,
    meta: { requiresCreator: true }
  },
  {
    path: '/user/:id/:code/edit',
    name: 'song_edit',
    component: song_edit,
    props: true,
    meta: { requiresCreator: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/forget_password',
    name: 'forgotpass',
    component: forgotpass
  },
  {
    path: '/api/login',
    name: 'login',
    component: login
  },
  {
    path: '/admin_login',
    name: 'admin_login',
    component: admin_login
  },
  {
    path: '/admin_support',
    name: 'admin_support',
    component: admin_support,
    meta: { requiresAdmin: true } 
  },
  {
    path: '/api/admin',
    name: 'admin_dashboard',
    component: admin_dashboard,
    meta: { requiresAdmin: true } 
  },
  {
    path: '/search/:query',
    name: 'search',
    component: search,
    props: true
  },
  {
    path: '/album/create',
    name: 'Album_Creation',
    component: album_create,
    meta: { requiresCreator: true }
  },
  {
    path: '/playlist/create',
    name: 'Playlist_Creation',
    component: playlist_create
  },
  {
    path: '/user_creator/:value',
    name: 'page_user',
    component: user_data,
    props: true
  },
  {
    path: '/album/:id/:value/view',
    name: 'albply_view',
    component: albply,
    props: true
  },
  {
    path: '/creator',
    name: 'page_creator',
    component: page_creator,
    meta: { requiresCreator: true }    
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

//___RBAC_for_Creator

router.beforeEach((to, from, next) => {
  const user = JSON.parse(localStorage.getItem('user')); 
  if (to.meta.requiresCreator) {    
    if (user.role == 'creator') {      
      if (user.usflag == 1) {        
        next({ path: '/policy' });
      } else {
        // Proceed to the route if user is authenticated and has sufficient role
        next();
      }
    } else {
      // Redirects to login if user is not authenticated or has insufficient role
      //next({ name: 'login' });
      next({ path: '/user_creator/1' });
    }
  } else {    
    next();
  }
});

//_____RBAC_for_Admin_____

router.beforeEach((to, from, next) => {
  const user = JSON.parse(localStorage.getItem('user')); 
  if (to.meta.requiresAdmin) {    
    if (user && user.role === 'admin') {       
      // Redirects to admin support page if user is an admin
      next({ path: '/admin_support' });      
    } else if (!user || !user.role) {
      // Redirects to login if user is not authenticated or role is not defined
      next({ name: 'login' });
    } else {
      // Proceed to the route if user is authenticated and not an admin
      next();
    }
  } else {    
    // Proceed to non-protected routes
    next();
  }
});


export default router
