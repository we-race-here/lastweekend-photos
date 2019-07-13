import Api from "@/endpoint/Api";

export default {
  get() {
    let params = {'page_size': 0};
    return Api.get("event", {'params': params});
  }
};
