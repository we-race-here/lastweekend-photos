// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from "vue";
import $ from "jquery";
import axios from "axios";
import BootstrapVue from "bootstrap-vue";

import Qs from "qs";

import router from "./router";
import store from "./store";
import App from "./App";
import { Config } from "./Config";
import { UI_VERSION_HEADER_NAME } from "./Constants";
import UtilMixin from "./components/mixins/UtilMixin";
import "./validators";

import "./filters";
import { version as AppVersion } from "../package.json";

Vue.use(BootstrapVue);

Vue.prototype.$eventsBus = new Vue();

/****************************************
 ****************** App *****************
 ****************************************/
axios.defaults.baseURL = Config.API_BASE_URL;
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.withCredentials = true; // allow to pass cookie in cross origin
axios.interceptors.request.use(function(request) {
  if (request.method === "get") {
    var r = UtilMixin.methods.randomId();
    request.url = UtilMixin.methods.addQSParm(request.url, "nc", r); // add nc param to avoid caching
  }
  return request;
});
function checkMismatchVersion(response) {
  let newVersion = response.headers[UI_VERSION_HEADER_NAME];
  if (newVersion && newVersion !== app.$appVersion) {
    app.$eventsBus.$emit("ui:mismatch-version", newVersion);
  }
}
axios.interceptors.response.use(
  function(response) {
    checkMismatchVersion(response);
    return response;
  },
  function(error) {
    if (401 === error.response.status) {
      if (app.$store.getters.isLoadedUser) {
        app.$eventsBus.$emit(
          "user:session-expired",
          app.$store.state.currentUser
        );
      }
    }
    checkMismatchVersion(error.response);
    return Promise.reject(error);
  }
);
axios.defaults.paramsSerializer = function(params) {
  return Qs.stringify(params, { arrayFormat: "repeat" });
};

Vue.prototype.$http = axios;
Vue.prototype.$publicPath = process.env.BASE_URL;
Vue.prototype.$appVersion = AppVersion;

var app = new Vue({
  el: "#app",
  template: "<App/>",
  components: { App },
  store: store,
  router: router,
  data: {},
  mixins: [UtilMixin],
  methods: {},
  created: function() {
    var self = this;
    /*this.$store.watch(
      function(state) {
        return state.currentUser;
      },
      function(newUser) {
      }
    );*/
    this.$http.get("session").then(
      function(response) {
        self.$store.state.currentUser = response.data;
        $("body").removeClass("kt-page--loading2");
      },
      function(error) {
        if (401 === (error.response && error.response.status)) {
          $("body").removeClass("kt-page--loading2");
        } else {
          self.showDefaultServerError(error, undefined, 0);
        }
      }
    );
  },
  mounted: function() {}
});
