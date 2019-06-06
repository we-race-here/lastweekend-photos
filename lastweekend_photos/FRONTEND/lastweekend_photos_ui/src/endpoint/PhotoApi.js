import Api from "@/endpoint/Api";

export default {
  getAll(params) {
    params = params || {};
    return Api.get("photo", {'params': params});
  },
  getMine(params) {
    params = params || {};
    return Api.get("photo/my", {'params': params});
  },
  upload(photo) {
    return Api.post("photo", photo);
  },
  delete(photo) {
    return Api.delete("photo/" + photo.id);
  }
};
