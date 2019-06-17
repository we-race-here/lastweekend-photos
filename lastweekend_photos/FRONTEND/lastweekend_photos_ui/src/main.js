// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from "vue";
import $ from "jquery";
import BootstrapVue from "bootstrap-vue";

import router from "./router";
import store from "./store";
import App from "./App";
import UtilMixin from "./components/mixins/UtilMixin";
import "./validators";
import SessionApi from "./endpoint/SessionApi"

import "./filters";
import { version as AppVersion } from "../package.json";

require("vue-multiselect/dist/vue-multiselect.min.css");

Vue.use(BootstrapVue);

Vue.prototype.$eventsBus = new Vue();

/****************************************
 ****************** App *****************
 ****************************************/

Vue.prototype.$publicPath = process.env.BASE_URL;
Vue.prototype.$appVersion = AppVersion;

new Vue({
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
    SessionApi.getUser().then(
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
