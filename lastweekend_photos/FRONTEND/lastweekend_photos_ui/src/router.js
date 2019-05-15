/****************************************
 ***************** Router ***************
 ****************************************/
import Vue from "vue";
import VueRouter from "vue-router";

import Dashboard from "./components/pages/Dashboard";
import MyProfile from "./components/pages/MyProfile";
import MyPhotos from "./components/pages/MyPhotos";
import Download from "./components/pages/Download";

Vue.use(VueRouter);

export const routeNames = {
  ROOT: "root",
  DASHBOARD: "dashboard",
  MY_PROFILE: "my-profile",
  MY_PHOTOS: "my-photos",
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
      redirect: {name: routeNames.DASHBOARD}
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
      path: "/dashboard",
      name: routeNames.DASHBOARD,
      meta: {
        pageInfo: {
          title: "Dashboard",
          titleDesc: "reports & statistics"
        }
      },
      component: Dashboard
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
      path: "/download",
      name: routeNames.DOWNLOAD,
      meta: {
        pageInfo: {
          title: "Download",
          titleDesc: "download photo"
        }
      },
      component: Download
    },
    {
      path: "*",
      redirect: {name: routeNames.DASHBOARD}
    }
  ]
});

router.afterEach(function (toRoute) {
  let title = "Lastweekend-Photos :: ",
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