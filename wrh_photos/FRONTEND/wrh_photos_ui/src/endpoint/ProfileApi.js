import Api from "@/endpoint/Api";

export default {
  get(){
    return Api.get("me");
  },
  update(body) {
    return Api.put("me", body);
  }
};
