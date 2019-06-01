<style scoped>
</style>

<template>
  <div>
    <page-bar></page-bar>
    <div class="kt-portlet kt-portlet--tabs">
      <div class="kt-portlet__head">
        <div class="kt-portlet__head-toolbar">
          <ul class="nav nav-tabs nav-tabs-line nav-tabs-line-brand nav-tabs-line-2x nav-tabs-line-right nav-tabs-bold"
              role="tablist">
            <li class="nav-item">
              <a class="nav-link active" data-toggle="tab" href="#myprofile_1_tab_content" role="tab">
                <i class="fas fa-user" aria-hidden="true"></i>Basic Info
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" data-toggle="tab" href="#myprofile_2_tab_content" role="tab">
                <i class="fas fa-camera" aria-hidden="true"></i>Photographer Profile
                <i v-if="profile.is_photographer" class="la la-check-circle text-success"></i>
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" data-toggle="tab" href="#myprofile_3_tab_content" role="tab">
                <i class="fab fa-adversal" aria-hidden="true"></i>Sponsor Profile
                <i v-if="profile.is_sponsor" class="la la-check-circle text-success"></i>
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" data-toggle="tab" href="#myprofile_4_tab_content" role="tab">
                <i class="fas fa-key" aria-hidden="true"></i>Change Password
              </a>
            </li>
          </ul>
        </div>
      </div>
      <div class="kt-portlet__body">
        <div class="tab-content">
          <div class="tab-pane active" id="myprofile_1_tab_content" role="tabpanel">
            <form class="kt-form kt-form--label-right" @submit.prevent="saveProfileInfo('basic')">
              <div class="kt-section kt-section--first">
                <div class="kt-section__body">
                  <div class="form-group kt-form__group row">
                    <div class="col-md-2"></div>
                    <div class="col-md-6">
                      <div class="kt-card-profile__pic-wrapper">
                        <img class="img-thumbnail thumbnail-photo"
                             :src="profileChosenFileData || profile.avatar || `${$publicPath}resources/images/avatar_blank.jpg`"
                             alt="">
                      </div>
                      <div>
                        <button v-if="profile.avatar" type="button" title="Delete Avatar"
                                class="btn btn-sm btn-danger btn-icon kt-margin-r-5"
                                :disabled="savingProfile" @click="profile.avatar=null">
                          <i class="la la-trash"></i>
                        </button>
                        <label class="btn btn-primary btn-sm kt-margin-0 kt-margin-r-5 pointer-cursor btn-icon"
                               title="Choose Avatar Image" :disabled="savingProfile">
                          <span class="la la-pencil"></span>
                          <input type="file" id="profile_image" name="profile_image" accept="image/jpeg, image/png"
                                 class="kt-hidden" @change="onChangeProfileFile">
                        </label>
                        <span v-if="profileChosenFile">{{ profileChosenFile.name }}
                          <a href="javascript:" @click="clearChosenAvatar"
                             title="Clear chosen image"><span
                                  class="la la-close"></span></a>
                        </span>
                        <span v-if="!profileChosenFile" class="text-muted">No Image Chosen</span>
                      </div>
                    </div>
                  </div>
                  <div class="form-group kt-form__group row">
                    <label class="col-md-2 col-form-label">Username:</label>
                    <div class="col-md-6">
                      <input type="text" class="form-control" disabled :value="profile.username"/>
                    </div>
                  </div>
                  <div class="form-group kt-form__group row">
                    <label class="col-md-2 col-form-label">Email:</label>
                    <div class="col-md-6">
                      <input type="email" class="form-control" disabled :value="profile.email"/>
                    </div>
                  </div>
                  <div class="form-group kt-form__group row">
                    <label class="col-md-2 col-form-label">First Name:</label>
                    <div class="col-md-6">
                      <input type="text" class="form-control" placeholder="First Name" v-model="profile.first_name">
                    </div>
                  </div>
                  <div class="form-group kt-form__group row">
                    <label class="col-md-2 col-form-label">Last Name:</label>
                    <div class="col-md-6">
                      <input type="text" class="form-control" placeholder="Last Name" v-model="profile.last_name">
                    </div>
                  </div>
                  <div class="form-group kt-form__group row">
                    <label class="col-md-2 col-form-label">Birth Date</label>
                    <div class="col-md-6">
                      <div class="input-group date">
                        <vue-datetimepicker v-model="profile.birth_date"
                                            placeholder="Birth Date (yyyy-mm-dd)"
                                            :wrap="true"
                                            name="birth_date"
                                            :config="{format: 'YYYY-MM-DD', mask: true, timepicker: false, scrollInput: false, iconRef: '.input-group-append'}"></vue-datetimepicker>
                        <div class="input-group-append pointer-cursor">
                          <span class="input-group-text"><i class="la la-calendar-o"></i></span>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="form-group kt-form__group row">
                    <label class="col-md-2 col-form-label">Gender:</label>
                    <div class="col-md-6">
                      <div class="kt-radio-inline">
                        <label class="kt-radio kt-radio--brand" v-for="g in genderOptions" :key="g.value">
                          <input type="radio" v-model="profile.gender" :value="g.value">{{ g.title }}
                          <span></span>
                        </label>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="kt-portlet__foot">
                <div class="kt-form__actions">
                  <div class="row">
                    <div class="col-md-2"></div>
                    <div class="col-md-6">
                      <button type="submit" name="submitBtn" class="btn btn-success kt-margin-r-5"
                              :disabled="errors.any() || savingProfile">
                        <i :class="savingProfile? 'la la-spin la-spinner':'la la-save'"></i>
                        <span v-show="!savingProfile">Save</span>
                        <span v-show="savingProfile">Saving</span>
                      </button>
                      <a is="router-link" :to="{name: $rns.DASHBOARD}" class="btn btn-secondary">Cancel </a>
                    </div>
                  </div>
                </div>
              </div>
            </form>
          </div>
          <div class="tab-pane" id="myprofile_2_tab_content" role="tabpanel">
            <form class="kt-form kt-form--label-right" @submit.prevent="saveProfileInfo('photographer')">
              <div class="kt-section kt-section--first">
                <div class="kt-section__body">
                  <div class="form-group kt-form__group row">
                    <label class="col-md-2 col-form-label">Enabled?</label>
                    <div class="col-md-6">
                      <span class="kt-switch kt-switch--outline kt-switch--icon kt-switch--success">
                        <label>
                          <input type="checkbox" checked="checked" v-model="profile.is_photographer">
                          <span></span>
                        </label>
                      </span>
                    </div>
                  </div>
                  <div class="form-group kt-form__group row">
                    <label class="col-md-2 col-form-label">Phone</label>
                    <div class="col-md-6">
                      <input type="text" class="form-control" placeholder="Phone Number"
                             v-model="profile.photographer.phone">
                    </div>
                  </div>
                  <div class="form-group kt-form__group row">
                    <label class="col-md-2 col-form-label">Street Address</label>
                    <div class="col-md-6">
                      <input type="text" class="form-control" placeholder="Street Address"
                             v-model="profile.photographer.street_address">
                    </div>
                  </div>
                  <div class="form-group kt-form__group row">
                    <label class="col-md-2 col-form-label">Country</label>
                    <div class="col-md-6">
                      <input type="text" class="form-control" placeholder="Country"
                             v-model="profile.photographer.country">
                    </div>
                  </div>
                  <div class="form-group kt-form__group row">
                    <label class="col-md-2 col-form-label">City</label>
                    <div class="col-md-6">
                      <input type="text" class="form-control" placeholder="City" v-model="profile.photographer.city">
                    </div>
                  </div>
                  <div class="form-group kt-form__group row">
                    <label class="col-md-2 col-form-label">State</label>
                    <div class="col-md-6">
                      <input type="text" class="form-control" placeholder="State" v-model="profile.photographer.state">
                    </div>
                  </div>
                  <div class="form-group kt-form__group row">
                    <label class="col-md-2 col-form-label">Zip Code</label>
                    <div class="col-md-6">
                      <input type="text" class="form-control" placeholder="Zip Code"
                             v-model="profile.photographer.zipcode">
                    </div>
                  </div>
                </div>
              </div>
              <div class="kt-portlet__foot">
                <div class="kt-form__actions">
                  <div class="row">
                    <div class="col-md-2"></div>
                    <div class="col-md-6">
                      <button type="submit" name="submitBtn" class="btn btn-success kt-margin-r-5"
                              :disabled="errors.any() || savingProfile">
                        <i :class="savingProfile? 'la la-spin la-spinner':'la la-save'"></i>
                        <span v-show="!savingProfile">Save</span>
                        <span v-show="savingProfile">Saving</span>
                      </button>
                      <a is="router-link" :to="{name: $rns.DASHBOARD}" class="btn btn-secondary">Cancel </a>
                    </div>
                  </div>
                </div>
              </div>
            </form>
          </div>
          <div class="tab-pane" id="myprofile_3_tab_content" role="tabpanel">
            <form class="kt-form kt-form--label-right" @submit.prevent="saveProfileInfo('sponsor')">
              <div class="kt-section kt-section--first">
                <div class="kt-section__body">
                  <div class="form-group kt-form__group row">
                    <label class="col-md-2 col-form-label">Enabled?</label>
                    <div class="col-md-6">
                      <span class="kt-switch kt-switch--outline kt-switch--icon kt-switch--success">
                        <label>
                          <input type="checkbox" checked="checked" v-model="profile.is_sponsor">
                          <span></span>
                        </label>
                      </span>
                    </div>
                  </div>
                  <div class="form-group kt-form__group row">
                    <label class="col-md-2 col-form-label">Brand Name</label>
                    <div class="col-md-6">
                      <input type="text" class="form-control" placeholder="Brand Name"
                             v-model="profile.sponsor.brand_name">
                    </div>
                  </div>
                  <div class="form-group kt-form__group row">
                    <label class="col-md-2 col-form-label">Phone</label>
                    <div class="col-md-6">
                      <input type="text" class="form-control" placeholder="Phone Number"
                             v-model="profile.sponsor.phone">
                    </div>
                  </div>
                  <div class="form-group kt-form__group row">
                    <label class="col-md-2 col-form-label">Street Address</label>
                    <div class="col-md-6">
                      <input type="text" class="form-control" placeholder="Street Address"
                             v-model="profile.sponsor.street_address">
                    </div>
                  </div>
                  <div class="form-group kt-form__group row">
                    <label class="col-md-2 col-form-label">Country</label>
                    <div class="col-md-6">
                      <input type="text" class="form-control" placeholder="Country" v-model="profile.sponsor.country">
                    </div>
                  </div>
                  <div class="form-group kt-form__group row">
                    <label class="col-md-2 col-form-label">City</label>
                    <div class="col-md-6">
                      <input type="text" class="form-control" placeholder="City" v-model="profile.sponsor.city">
                    </div>
                  </div>
                  <div class="form-group kt-form__group row">
                    <label class="col-md-2 col-form-label">State</label>
                    <div class="col-md-6">
                      <input type="text" class="form-control" placeholder="State" v-model="profile.sponsor.state">
                    </div>
                  </div>
                  <div class="form-group kt-form__group row">
                    <label class="col-md-2 col-form-label">Zip Code</label>
                    <div class="col-md-6">
                      <input type="text" class="form-control" placeholder="Zip Code" v-model="profile.sponsor.zipcode">
                    </div>
                  </div>
                </div>
              </div>
              <div class="kt-portlet__foot">
                <div class="kt-form__actions">
                  <div class="row">
                    <div class="col-md-2"></div>
                    <div class="col-md-6">
                      <button type="submit" name="submitBtn" class="btn btn-success kt-margin-r-5"
                              :disabled="errors.any() || savingProfile">
                        <i :class="savingProfile? 'la la-spin la-spinner':'la la-save'"></i>
                        <span v-show="!savingProfile">Save</span>
                        <span v-show="savingProfile">Saving</span>
                      </button>
                      <a is="router-link" :to="{name: $rns.DASHBOARD}" class="btn btn-secondary">Cancel </a>
                    </div>
                  </div>
                </div>
              </div>
            </form>
          </div>
          <div class="tab-pane" id="myprofile_4_tab_content" role="tabpanel">
            <form class="kt-form kt-form--label-right" @submit.prevent="changePassword">
              <div class="kt-section kt-section--first">
                <div class="kt-section__body">
                  <div class="form-group kt-form__group row">
                    <label class="col-md-2 col-form-label">Current Password</label>
                    <div class="col-md-6">
                      <input name="current_password" type="password" class="form-control"
                             placeholder="Current Password" v-model="userPassword.current_password" required/>
                    </div>
                  </div>
                  <div class="form-group kt-form__group row">
                    <label class="col-md-2 col-form-label">New Password</label>
                    <div class="col-md-6">
                      <input name="new_password" type="password" class="form-control"
                             placeholder="New Password" v-model="userPassword.new_password" required/>
                    </div>
                  </div>
                  <div class="form-group kt-form__group row">
                    <label class="col-md-2 col-form-label">Re-Type New Password</label>
                    <div class="col-md-6">
                      <input name="re_new_password" type="password" class="form-control"
                             placeholder="Re-Type New Password" v-model="userPassword.re_new_password" required/>
                      <span class="help-block text-danger"
                            v-show="!passwordMatched"> Mismatched re-type password </span>
                    </div>
                  </div>
                </div>
              </div>
              <div class="kt-portlet__foot">
                <div class="kt-form__actions">
                  <div class="row">
                    <div class="col-md-2"></div>
                    <div class="col-md-6">
                      <button type="submit" name="submitBtn" class="btn btn-success kt-margin-r-5"
                              :disabled="!userPassword.new_password || !passwordMatched || changingPassword">
                        <i :class="changingPassword? 'la la-spin la-spinner':'la la-key'"></i>
                        <span v-show="!changingPassword">Change Password</span>
                        <span v-show="changingPassword">Changing</span>
                      </button>
                      <a is="router-link" :to="{name: $rns.DASHBOARD}" class="btn btn-secondary">Cancel </a>
                    </div>
                  </div>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import $ from "jquery";
  import UtilMixin from "../mixins/UtilMixin";
  import VueDatetimepicker from "../libs/VueDatetimepicker";
  import LoadingOverlayableMixin from "../mixins/LoadingOverlayableMixin";
  import PageBar from "../partials/PageBar";
  import {GENDER_OPTIONS} from "../../Constants";
  import ProfileApi from "../../endpoint/ProfileApi"

  const moment = window.moment;

  export default {
    mixins: [UtilMixin, LoadingOverlayableMixin],
    components: {PageBar, VueDatetimepicker},
    data: function () {
      return {
        profileChosenFile: null,
        profileChosenFileData: null,
        deletingAvatar: false,
        savingProfile: false,
        changingPassword: false,
        genderOptions: GENDER_OPTIONS,
        userPassword: {
          current_password: "",
          new_password: "",
          re_new_password: ""
        },
        profile: {
          photographer: {},
          sponsor: {},
        }
      };
    },
    created: function () {
      var self = this;
      this.loadingOverlay = true;
      ProfileApi.get().then(
          function (response) {
            self.profile = response.data;
            self.loadingOverlay = false;
          },
          function (error) {
            self.showDefaultServerError(error);
            self.loadingOverlay = false;
          }
      );
    },
    computed: {
      passwordMatched: function () {
        return (
            this.userPassword.new_password === this.userPassword.re_new_password
        );
      }
    },
    methods: {
      clearChosenAvatar: function () {
        this.profileChosenFile = null;
        this.profileChosenFileData = null;
        $("#profile_image").val("");
      },
      onChangeProfileFile: function (event) {
        if (event.target.files.length > 0) {
          this.profileChosenFile = event.target.files[0];
          var f = this.profileChosenFile,
              self = this,
              r = new FileReader();
          r.onloadend = function (e) {
            self.profileChosenFileData = e.target.result;
          };
          r.readAsDataURL(f);

        }
      },
      getProfilePostData: function (profileType) {
        var postData = {},
            self = this;
        if (profileType === "basic") {
          ["first_name", "last_name", "gender", "birth_date", "avatar"].forEach(function (f) {
            postData[f] = self.profile[f];
          });
          if (postData.birth_date && typeof postData.birth_date === "object") {
            postData.birth_date = moment(postData.birth_date).format("YYYY-MM-DD");
          }
          if (this.profileChosenFileData) {
            postData.avatar = this.profileChosenFileData;
          } else if (postData.avatar !== null) {
            delete postData.avatar;
          }
        } else if (profileType === "photographer") {
          postData["photographer"] = this.profile.photographer || {};
          postData["is_photographer"] = this.profile.is_photographer === true;
        } else if (profileType === "sponsor") {
          postData["sponsor"] = this.profile.sponsor || {};
          postData["is_sponsor"] = this.profile.is_sponsor === true;
        }
        return postData;
      },
      saveProfileInfo: function (profileType) {
        var self = this;
        this.savingProfile = true;
        var postData = this.getProfilePostData(profileType || "basic");
        this.savingProfile = true;
        ProfileApi.update(postData).then(
            function (response) {
              self.profile = response.data;
              self.$store.state.currentUser.avatar = self.profile.avatar;
              self.savingProfile = false;
              self.clearChosenAvatar();
              self.showSuccess("Profile updated successfully", 5000);
            },
            function (error) {
              self.savingProfile = false;
              self.showDefaultServerError(error);
            }
        );
      },
      changePassword: function () {
        var self = this;
        this.changingPassword = true;
        this.$http.put("me/password", this.userPassword).then(
            function () {
              self.userPassword = {};
              self.changingPassword = false;
              self.showSuccess("Password changed successfully", 5000);
            },
            function (response) {
              self.changingPassword = false;
              self.showDefaultServerError(response, true);
            }
        );
      }
    }
  };
</script>
