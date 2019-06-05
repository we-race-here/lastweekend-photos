import Api from "@/endpoint/Api";

export default {
  get() {
    let params = {'page_size': 0};
    return Api.get("photo_tag", {'params': params});
  },
  add(tag) {
    return Api.post("photo_tag", tag);
  },
  delete(tag) {
    return Api.delete("photo_tag/" + tag.id);
  }
};
