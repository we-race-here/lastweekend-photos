import Api from "@/endpoint/Api";

export default {
  get(params) {
    params = params || {};
    return Api.get("photo", {'params': params});
  }
};
