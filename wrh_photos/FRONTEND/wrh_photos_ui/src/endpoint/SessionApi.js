import Api from "@/endpoint/Api";

export default {
  getUser() {
    return Api.get("session");
  },
  singIn(signInForm) {
    return Api.post("session", signInForm);
  },
  logout() {
    return Api.delete("session");
  }
};
