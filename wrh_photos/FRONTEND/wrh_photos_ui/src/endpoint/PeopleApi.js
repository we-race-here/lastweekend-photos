import Api from "@/endpoint/Api";

export default {
  get() {
    let params = {'page_size': 0};
    return Api.get("photo_people", {'params': params});
  },
  add(tag) {
    return Api.post("photo_people", tag);
  },
  delete(tag) {
    return Api.delete("photo_people/" + tag.id);
  }
};
