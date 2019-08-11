import axios from "axios";
import {Config} from "../Config";
import EventBus from "../event-bus";
import {UI_VERSION_HEADER_NAME} from "../Constants";
import { version as AppVersion } from "../../package.json";
import Qs from "qs";
import UtilMixin from "../components/mixins/UtilMixin";

function checkMismatchVersion(response) {
  let newVersion = response.headers[UI_VERSION_HEADER_NAME];
  if (newVersion && newVersion !== AppVersion) {
    EventBus.$emit("ui:mismatch-version", newVersion);
  }
}

const axiosInstance = axios.create({
  baseURL: Config.API_BASE_URL,
  timeout: Config.DEFAULT_AXIOS_TIMEOUT,
  xsrfCookieName: "csrftoken",
  xsrfHeaderName: "X-CSRFToken",
  withCredentials: true,
  paramsSerializer: function (params) {
    return Qs.stringify(params, {arrayFormat: "repeat"});
  },
  headers: {
    "Content-Type": "application/json"
  }
});

axiosInstance.interceptors.response.use(function (response) {
      checkMismatchVersion(response);
      return response;
    }, function (error) {
      if (401 === error.response.status) {
        EventBus.$emit("user:session-expired");
      }
      checkMismatchVersion(error.response);
      return Promise.reject(error);
    }
);
axios.interceptors.request.use(function (request) {
  if (request.method === "get") {
    let r = UtilMixin.methods.randomId();
    request.url = UtilMixin.methods.addQSParm(request.url, "nc", r); // add nc param to avoid caching
  }
  return request;
});

export default axiosInstance;
