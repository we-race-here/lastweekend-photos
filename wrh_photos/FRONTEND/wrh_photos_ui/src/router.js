/****************************************
 ***************** Router ***************
 ****************************************/
import Vue from "vue";
import VueRouter from "vue-router";

import PhotoList from "./components/pages/PhotoList";
import MyProfile from "./components/pages/MyProfile";
import MyPhotos from "./components/pages/MyPhotos";
import store from "./store";

Vue.use(VueRouter);

export const routeNames = {
  ROOT: "root",
  DASHBOARD: "dashboard",
  INDEX_PAGE: "index_page",
  MY_PROFILE: "my_profile",
  MY_PHOTOS: "my_photos",
  DOWNLOAD:'download',
};

Vue.prototype.$rns = routeNames;

const router = new VueRouter({
  scrollBehavior: function (to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return {x: 0, y: 0};
    }
  },
  routes: [
    {
      path: "/",
      name: routeNames.ROOT,
      redirect: {name: routeNames.INDEX_PAGE},
      meta: {
        public: true
      }
    },
    {
      path: "/index",
      name: routeNames.INDEX_PAGE,
      meta: {
        public: true,
        pageInfo: {
          title: "Photo List",
          titleDesc: "list of photos"
        }
      },
      component: PhotoList
    },
    {
      path: "/my-profile",
      name: routeNames.MY_PROFILE,
      meta: {
        pageInfo: {
          title: "My Profile",
          titleDesc: "user profile info"
        }
      },
      component: MyProfile
    },
    {
      path: "/my-photos",
      name: routeNames.MY_PHOTOS,
      meta: {
        pageInfo: {
          title: "My Photos",
          titleDesc: "manage photos"
        }
      },
      component: MyPhotos
    },
    {
      path: "*",
      redirect: {name: routeNames.INDEX_PAGE}
    }
  ]
});

router.beforeEach(function(to, from, next) {
  if (store.getters.isLoadedUser || (to.meta || {}).public) {
    next();
  } else {
    next({ name: routeNames.ROOT, replace: true });
  }
});

router.afterEach(function (toRoute) {
  let title = "WRH/Photos :: ",
      pageInfo = toRoute.meta.pageInfo || {};
  if (pageInfo.title) {
    title = title + pageInfo.title + " :: ";
  }
  if (pageInfo.titleDesc) {
    title = title + pageInfo.titleDesc;
  }
  window.document.title = title;
});

export default router;
