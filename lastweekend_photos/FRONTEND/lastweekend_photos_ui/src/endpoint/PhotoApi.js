import Api from "@/endpoint/Api";

export default {
  get(params) {
    params = params || {};
    params['page_size'] = 0;

    return Api.get("photo", {'params': params});
  }
};
