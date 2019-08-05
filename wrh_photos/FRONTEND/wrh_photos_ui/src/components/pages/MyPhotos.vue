<template>
  <div class="kt-container kt-container--fluid  kt-grid__item kt-grid__item--fluid">
    <page-bar></page-bar>
    <div class="kt-portlet">
      <div class="kt-portlet__head">
        <div class="kt-subheader kt-grid__item" id="kt_subheader_search_container">
          <div class="kt-subheader__main">
            <div class="container-fluid">
              <div class="row justify-content-md-center align-items-center">
                <div class="col-auto mt-1 p-0">
                  <span class="kt-subheader__desc" id="kt_subheader_total">{{photos.pagination.total}} Total</span>
                </div>
                <div class="col-md-6 col-sm-10 p-0 mr-auto kt-subheader__group" id="kt_subheader_search">
                  <div class="kt-input-icon kt-input-icon--right kt-subheader__search mr-3">
                    <input type="text" class="form-control" placeholder="Search..." id="generalSearch"
                           v-model="searchValue">
                    <span class="kt-input-icon__icon kt-input-icon__icon--right">
                      <span><i class="flaticon2-search-1"></i></span>
                    </span>
                  </div>
                  <div class="kt-subheader__search event-select">
                    <multiselect v-model="searchSelectedEvents" :options="events" :multiple="true" track-by="id"
                                 label="name"
                                 placeholder="Select event">
                    </multiselect>
                  </div>
                </div>
                <div class="col-md-auto col-sm-12 p-0">
                  <button type="button" class="btn btn-outline-brand btn-sm"
                          @click="openAddPhotoModal">
                    <i class="flaticon2-plus"></i>
                    Add photo
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="kt-portlet__body">
        <div class="container-fluid mr-3 ml-3">
          <div class="row">
            <div class="col-md-3 mt-3 mb-3" v-for="photo in photos.results" :key="photo.id">
              <div class="kt-portlet">
                <div class="kt-portlet__head">
                  <div class="kt-portlet__head-label">
                              <span class="kt-portlet__head-icon">
                                <i class="la la-user large-icon"></i>
                              </span>
                    <h3 class="kt-portlet__head-title">
                      {{photo.title}}
                    </h3>
                  </div>
                  <div class="kt-portlet__head-toolbar">
                    <div class="kt-portlet__head-actions">
                      <button type="button" @click="openEditPhotoModal(photo)"
                              class="btn btn-outline-success btn-sm btn-icon btn-icon-md mr-1">
                        <i class="flaticon-edit"></i>
                      </button>
                      <button type="button" @click="showConfirmDeleteModal(photo)"
                              class="btn btn-outline-danger btn-sm btn-icon btn-icon-md mr-1">
                        <i class="flaticon-delete"></i>
                      </button>
                    </div>
                  </div>
                </div>
                <div class="kt-portlet__body">
                  <img :src="photo.preview_file" class="size-auto"/>
                </div>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col">
              <b-pagination size="lg" :total-rows="photos.pagination.total" v-model="currentPage"
                            :per-page="pageSize" first-text="First"
                            prev-text="Prev"
                            next-text="Next"
                            last-text="Last"
                            align="center"
                            @input="getPhotos(searchValue, searchSelectedEvents, currentPage, pageSize)">
              </b-pagination>
            </div>
          </div>
        </div>
      </div>

      <!-- Add/Edit photo modal -->
      <b-modal
              size="lg"
              centered
              ref="addEditPhotoModalRef"
              id="addEditPhotoModal"
              :title="photoModalType === PhotoModalType.Add ? 'Add photo(s)' : 'Edit the photo'"
              @hide="onAddEditPhotoModalHide"
              :hide-footer="true">
        <div class="modal-body">
          <div class="row">
            <div class="col-md-6 col-sm-12">
              <div class="row">
                <div class="kt-portlet kt-portlet--bordered">
                  <div class="kt-portlet__head">
                    <div class="kt-portlet__head-label">
                      <h5>{{selectedPhotos[0].name === unknownFileName ? 0 : selectedPhotos.length}} photo(s)
                        selected</h5>
                    </div>
                    <div class="kt-portlet__head-toolbar">
                      <div class="kt-portlet__head-actions">
                        <div class="upload-btn-wrapper" v-if="photoModalType === PhotoModalType.Add">
                          <label class="btn btn-outline-brand btn-sm pointer-cursor">
                            Select photo(s)
                            <input type="file" ref="selectedPhotosRef" @change="selectPhotos" multiple accept="image/*"
                                   class="kt-hidden"/>
                          </label>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="kt-portlet__body">
                    <img :src="(selectedPhotos[selectedPhotoIndex] || {}).original_file  ||
                    (selectedPhotos[selectedPhotoIndex] || {}).preview_file ||
                    `${$publicPath}resources/images/no-photo-available.png`"
                         class="size-auto-fix"/>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-md-6 col-sm-12 pr-0">
              <div class="row">
                <div class="col">
                  <div class="row">
                    <div class="col">
                      <input type="text" class="form-control" v-model="selectedPhotos[selectedPhotoIndex].title"
                             placeholder="Pick a name for your photo">
                    </div>
                  </div>
                  <div class="row mt-2">
                    <div class="col">
                      <textarea aria-multiline="true" class="form-control"
                                v-model="selectedPhotos[selectedPhotoIndex].description"
                                placeholder="Add a description">
                      </textarea>
                    </div>
                  </div>
                  <div class="row mt-2">
                    <div class="col">
                      <input type="text" class="form-control" v-model="selectedPhotos[selectedPhotoIndex].price"
                             placeholder="Price">
                    </div>
                    <div class="col">
                      <div class="dropdown">
                        <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton"
                                data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                          Logo position:
                          <span class="kt-font-bolder">
                            {{ logoPositionMap[selectedPhotos[selectedPhotoIndex].logo_position || 'br'].title }}
                          </span>
                        </button>
                        <div class="dropdown-menu" aria-labelledby="dropdownMenuButton" x-placement="top-start"
                             style="position: absolute; will-change: transform; top: 0; left: 0; transform: translate3d(0, -138px, 0);">

                          <a href="javascript:" v-for="p in logoPositionOptions" :key="p.value" class="dropdown-item"
                             :class="{active: p.value==(selectedPhotos[selectedPhotoIndex].logo_position || 'br')}"
                             data-toggle="kt-tooltip" data-placement="left" @click="onClickLogoPosition(p.value)">
                            {{ p.title }}
                          </a>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="row mt-2">
                    <div class="col">
                      <dateTime placeholder="Date of Photo"
                                v-model="selectedPhotos[selectedPhotoIndex].date"
                                :config="{ timepicker: false, format: 'YYYY/MM/DD' }"
                                comparator="date"
                      ></dateTime>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col mt-2">
                      <multiselect v-model="selectedPhotos[selectedPhotoIndex]._event" :options="events"
                                   :multiple="false" track-by="id"
                                   label="name"
                                   placeholder="Select events...">
                      </multiselect>
                    </div>
                  </div>
                  <div class="row mt-2">
                    <div class="col">
                      <multiselect v-model="selectedPhotos[selectedPhotoIndex]._tags" :options="tags"
                                   :multiple="true" track-by="id" label="name"
                                   placeholder="Select tags..." :loading="tagIsLoading" :taggable="true"
                                   tag-placeholder="Add this as new tag"
                                   @tag="addTag">
                      </multiselect>
                    </div>
                  </div>
                  <div class="row mt-2">
                    <div class="col">
                      <multiselect v-model="selectedPhotos[selectedPhotoIndex]._peoples" :options="people"
                                   :multiple="true" track-by="id"
                                   label="name"
                                   placeholder="Select people..."
                                   :taggable="true"
                                   :loading="peopleIsLoading"
                                   tag-placeholder="Add this as new people"
                                   @tag="addPeople"></multiselect>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="row mt-2"
               v-if="photoModalType === PhotoModalType.Add && selectedPhotos[0].name !== unknownFileName">
            <div class="col-auto navigation-arrow d-flex align-items-center"
                 :class="{'navigation-arrow-hover': selectedPhotoIndex > 0}" @click="previousPhoto">
              <i class="flaticon2-back"></i>
            </div>
            <div class="col p-0">
              <b-container fluid class="p-4 bg-dark">
                <b-row>
                  <b-col v-for="index in 10" :key="(index - 1) + selectedPhotoNavigationIndex">
                    <b-img fluid
                           v-bind:class="selectedPhotos[(index - 1) + selectedPhotoNavigationIndex].uploaded ? 'img-thumbnail-uploaded' : selectedPhotos[(index - 1) + selectedPhotoNavigationIndex].uploading ? 'img-thumbnail-uploading': (selectedPhotoIndex === (index - 1) + selectedPhotoNavigationIndex ? 'img-thumbnail-viewed' : '')"
                           v-if="selectedPhotos.length >= index + selectedPhotoNavigationIndex"
                           :src="selectedPhotos[(index - 1) + selectedPhotoNavigationIndex].original_file || selectedPhotos[(index - 1) + selectedPhotoNavigationIndex].preview_file"
                           @click="selectedPhotoIndex = (index - 1) + selectedPhotoNavigationIndex"></b-img>
                  </b-col>
                </b-row>
              </b-container>
            </div>
            <div class="col-auto navigation-arrow d-flex align-items-center"
                 :class="{'navigation-arrow-hover': selectedPhotoIndex < selectedPhotos.length - 1}"
                 @click="nextPhoto">
              <i class="flaticon2-next"></i>
            </div>
          </div>
          <div class="row">
            <div class="col p-0">
              <button class="btn btn-success btn-block btn-spinner btn-lg mt-3 mr-3" @click="uploadPhotos"
                      :disabled="anyUploading || allUploaded">
                <i :class="anyUploading? 'fa fa-spin fa-spinner':'fa fa-upload'"></i>
                <span v-show="!anyUploading">{{photoModalType === PhotoModalType.Add ? 'Upload' : 'Update'}}</span>
                <span v-show="anyUploading">{{photoModalType === PhotoModalType.Add ? 'Uploading' : 'Updating'}}</span>
                <span v-if="allUploaded" class="la la-check-circle"></span>
              </button>
            </div>
          </div>
        </div>
      </b-modal>

      <!-- Delete photo modal -->
      <b-modal
              centered
              ref="confirmDeleteModalRef"
              id="confirmDeleteModal"
              :hide-header="true"
      >
        <p class="text-danger h6">Are you sure to delete this photo?</p>
        <div slot="modal-footer" class="w-100">
          <button
                  type="button"
                  class="btn btn-secondary float-left"
                  @click="$refs.confirmDeleteModalRef.hide()"
          >
            <i class="la la-close"></i> Cancel
          </button>
          <button
                  type="button"
                  class="btn btn-danger float-right"
                  :disabled="deletingPhoto"
                  @click="deletePhoto"
          >
            <i
                    :class="deletingPhoto ? 'la la-spin la-spinner' : 'la la-trash'"
            ></i>
            <span v-show="!deletingPhoto">Delete</span>
            <span v-show="deletingPhoto">Deleting</span>
          </button>
        </div>
      </b-modal>
    </div>
  </div>
</template>

<script>
  import PageBar from "../partials/PageBar";
  import Multiselect from 'vue-multiselect'
  import UtilMixin from "../mixins/UtilMixin";
  import LoadingOverlayableMixin from "../mixins/LoadingOverlayableMixin";
  import EventApi from "../../endpoint/EventApi";
  import TagApi from "../../endpoint/TagApi";
  import PeopleApi from "../../endpoint/PeopleApi";
  import PhotoApi from "../../endpoint/PhotoApi";
  import dateTime from "../libs/VueDatetimepicker";
  import {
    LOGO_POSITION_OPTIONS, LOGO_POSITION_MAP
  } from "../../Constants";

  export default {
    name: "MyPhotos",
    components: {
      PageBar,
      Multiselect,
      dateTime
    },
    mixins: [
      UtilMixin, LoadingOverlayableMixin
    ],
    created: function () {
      // Retrieve event list
      EventApi.get().then((resp) => {
        this.events = resp.data.results;
      }, (resp) => {
        this.showMessage((resp.response && resp.response.data.detail) ||
            "Some error happened when trying to get events")
      });

      // Retrieve tag list
      TagApi.get().then((resp) => {
        this.tags = resp.data.results;
      }, (resp) => {
        this.showMessage((resp.response && resp.response.data.detail) ||
            "Some error happened when trying to get tags")
      });

      // Retrieve people list
      PeopleApi.get().then((resp) => {
        this.people = resp.data.results;
      }, (resp) => {
        this.showMessage((resp.response && resp.response.data.detail) ||
            "Some error happened when trying to get people")
      });

      // Retrieve photo list
      this.getPhotos(this.searchValue, this.searchSelectedEvents, this.currentPage, this.pageSize);
    },
    watch: {
      "searchSelectedEvents": function () {
        this.getPhotos(this.searchValue, this.searchSelectedEvents, this.currentPage, this.pageSize);
      },
      "searchValue": function () {
        // Debounce search request
        if (this.previousSearchTimeout) {
          clearTimeout(this.previousSearchTimeout);
        }
        this.previousSearchTimeout = setTimeout(() => {
          this.getPhotos(this.searchValue, this.searchSelectedEvents, this.currentPage, this.pageSize);
        }, 500)
      }
    },
    computed: {
      anyUploading: function () {
        return this.selectedPhotos.filter(f => f.uploading).length > 0;
      },
      allUploaded: function () {
        return this.selectedPhotos.length > 0 && this.selectedPhotos.filter(f => !f.uploaded).length === 0
      }
    },
    methods: {
      onClickLogoPosition: function (position) {
        this.$set(this.selectedPhotos[this.selectedPhotoIndex], 'logo_position', position);
      },
      getPhotos: function (searchValue, selectedEvents, currentPage, pageSize) {
        let params = {'search': searchValue, 'page': currentPage, 'page_size': pageSize};

        // Create events id
        if (selectedEvents.length > 0) {
          let ids = [];
          for (let i = 0; i < selectedEvents.length; i++) {
            ids.push(selectedEvents[i].id)
          }
          params['event'] = ids;
        }
        this.loadingOverlay = true;
        PhotoApi.getMine(params).then((resp) => {
          this.photos = resp.data;
          this.loadingOverlay = false;
        }, (resp) => {
          this.loadingOverlay = true;
          this.showMessage((resp.response && resp.response.data.detail) ||
              "Some error happened when trying to get my photo")
        })
      },
      openAddPhotoModal: function () {
        this.photoModalType = this.PhotoModalType.Add;
        this.$refs.addEditPhotoModalRef.show()
      },
      openEditPhotoModal: function (photo) {
        this.photoModalType = this.PhotoModalType.Edit;
        // To fix vue reactive property
        this.$set(photo, 'uploaded', false);
        this.$set(photo, 'uploading', false);
        this.addSelectedPhoto(photo);
        this.$refs.addEditPhotoModalRef.show()
      },
      selectPhotos: function () {
        // push select photo into the selected photo array
        for (let i = 0; i < this.$refs.selectedPhotosRef.files.length; i++) {
          let reader = new FileReader();
          let file = this.$refs.selectedPhotosRef.files[i];

          // Prevent duplicate file
          let isDuplicate = false;
          for (let j = 0; j < this.selectedPhotos.length; j++) {
            if (this.selectedPhotos[j].name === file.name) {
              isDuplicate = true;
              break;
            }
          }
          if (isDuplicate) {
            continue;
          }

          reader.onload = e => {
            let newPhoto = e.target.result;
            this.addSelectedPhoto({
              name: file.name,
              original_file: newPhoto,
              _event: {
                name: "Select an event..."
              },
              _tags: [],
              _peoples: [],
              uploaded: false,
              uploading: false,
            });
          };
          reader.readAsDataURL(file);
        }
        this.$refs.selectedPhotosRef.value = "";
      },
      uploadPhotos: function () {
        // At least the first photo must be has name, event, etc.
        if (this.selectedPhotos[0].name === this.unknownFileName) {
          return this.showError("No photo selected");
        }
        let defaultPhotoInfo = this.selectedPhotos[0];
        if (!(defaultPhotoInfo._event || {}).id) {
          return this.showError("No event chosen!");
        }
        if (!(defaultPhotoInfo.title || "").trim()) {
          return this.showError("No title entered!");
        }

        // Fix photo relations
        for (let i = 0; i < this.selectedPhotos.length; i++) {
          let uploadPhoto = this.selectedPhotos[i];
          if (uploadPhoto.uploaded) {
            continue;
          }
          // Each photo only correspond to one event
          uploadPhoto.event = (uploadPhoto._event || {}).id;

          uploadPhoto.tags = [];
          for (let j = 0; j < uploadPhoto._tags.length; j++) {
            uploadPhoto.tags.push(uploadPhoto._tags[j].id);
          }

          uploadPhoto.peoples = [];
          for (let j = 0; j < uploadPhoto._peoples.length; j++) {
            uploadPhoto.peoples.push(uploadPhoto._peoples[j].id);
          }

          // choose default value for unspecified ones
          let postData = Object.assign({}, uploadPhoto);
          ["title", "description", "event", "price", "logo_position", "photo_date"].forEach(function (f) {
            if (!postData[f]) {
              postData[f] = defaultPhotoInfo[f];
            }
          });
          if (!postData.tags.length) {
            postData.tags = defaultPhotoInfo.tags;
          }
          if (!postData.peoples.length) {
            postData.peoples = defaultPhotoInfo.peoples;
          }

          // Edit the photo if it already has id
          let uploadAction;
          if (postData.id > 0) {
            uploadAction = PhotoApi.edit(postData);
          } else {
            uploadAction = PhotoApi.add(postData);
          }

          uploadPhoto.uploading = true;
          uploadAction.then(() => {
                uploadPhoto.uploading = false;
                uploadPhoto.uploaded = true;
              }, () => {
                uploadPhoto.uploading = false;
                this.showError(`Some error happened when trying to upload ${uploadPhoto.name} photo`, 500);
              }
          )
        }
      },
      addTag: function (search) {
        this.tagIsLoading = true;
        TagApi.add({name: search}).then((resp) => {
          this.tags.push(resp.data);
          this.selectedPhotos[this.selectedPhotoIndex]._tags.push(resp.data);
          this.tagIsLoading = false;
        });
      },

      addPeople: function (search) {
        this.peopleIsLoading = true;
        PeopleApi.add({name: search}).then((resp) => {
          this.people.push(resp.data);
          this.selectedPhotos[this.selectedPhotoIndex]._peoples.push(resp.data);
          this.peopleIsLoading = false;
        });
      },
      onAddEditPhotoModalHide: function () {
        this.selectedPhotos = [
          {
            name: this.unknownFileName,
          }
        ];
        this.selectedPhotoIndex = 0;
        this.selectedPhotoNavigationIndex = 0;
        this.addEditModalTitle = "";
        this.getPhotos(this.searchValue, this.searchSelectedEvents, this.currentPage, this.pageSize);
      },
      showConfirmDeleteModal: function (photo) {
        this.selectedPhoto = photo;
        this.$refs.confirmDeleteModalRef.show();
      },
      deletePhoto() {
        this.deletingPhoto = true;
        PhotoApi.delete(this.selectedPhoto).then(() => {
          this.deletingPhoto = false;
          this.$refs.confirmDeleteModalRef.hide();
          this.photos.results.splice(
              this.photos.results.indexOf(this.selectedPhoto),
              1
          );
          this.getPhotos(this.searchValue, this.searchSelectedEvents, this.currentPage, this.pageSize);
          this.showSuccess("The photo deleted", 1000);
        }, (resp) => {
          this.deletingPhoto = false;
          this.showError(
              (resp.response && resp.response.data.detail) ||
              "Some error happened when trying to delete the photo", 1000
          );

        })
      },
      nextPhoto: function () {
        if (this.selectedPhotoIndex >= this.selectedPhotos.length - 1) {
          return
        }
        this.selectedPhotoIndex++;
        if (this.selectedPhotoIndex >= 10) {
          this.selectedPhotoNavigationIndex++;
        }
      },
      previousPhoto: function () {
        if (this.selectedPhotoIndex <= 0) {
          return
        }
        this.selectedPhotoIndex--;
        if (this.selectedPhotoIndex < this.selectedPhotoNavigationIndex) {
          this.selectedPhotoNavigationIndex--;
        }
      },
      addSelectedPhoto(photo) {
        this.selectedPhotos.push(photo);

        if (this.selectedPhotos.length > 1 &&
            this.selectedPhotos[0].name === this.unknownFileName) {
          this.selectedPhotos.splice(0, 1);
        }
      }
    },
    data: function () {
      const unknownFileName = "__unknown__";
      const PhotoModalType = {
        None: "none",
        Add: "add",
        Edit: "edit"
      };
      return {
        searchValue: "",
        logoPositionOptions: LOGO_POSITION_OPTIONS,
        logoPositionMap: LOGO_POSITION_MAP,
        previousSearchTimeout: null,
        selectedPhoto: {},
        photos: {
          pagination: {},
          results: []
        },
        searchSelectedEvents: [],
        events: [],
        selectedEvents: [],
        unknownFileName: unknownFileName,
        selectedPhotos: [
          {
            name: unknownFileName,
            logo_position: 'br'
          }
        ],
        selectedPhotoIndex: 0,
        selectedPhotoNavigationIndex: 0,
        tags: [],
        tagIsLoading: false,
        people: [],
        peopleIsLoading: false,
        currentPage: 1,
        pageSize: 12,
        deletingPhoto: false,
        photoModalType: PhotoModalType.None,
        PhotoModalType: PhotoModalType
      }
    }
  }
</script>

<style scoped>

  #generalSearch {
    font-size: 1rem !important;
  }

  .event-select {
    width: 70% !important;
    margin-top: 8px !important;
  }

  #kt_subheader_search_container .kt-subheader__main .kt-subheader__title {
    margin-top: 5px !important;
  }

  .large-icon {
    font-size: 1.75rem;
  }

  .size-auto {
    width: 100%;
    height: 250px;
    object-fit: cover;
    object-position: center center;
  }

  .size-auto-fix {
    width: 320px;
    height: 300px;
  }

  #kt_subheader_search_container {
    width: 100%;
  }

  .modal-full {
    height: 93%;
    display: flex;
    width: 100% !important;
    max-width: 100% !important;
    background-color: #ffffff;
  }

  .modal-content {
    background-color: transparent;
    color: white;
  }

  .upload-btn-wrapper {
    position: relative;
    overflow: hidden;
    display: inline-block;
  }

  .btn-file {
    border: 2px solid gray;
    color: gray;
    background-color: white;
    padding: 8px 20px;
    border-radius: 8px;
    font-size: 20px;
    font-weight: bold;
  }

  .upload-btn-wrapper input[type=file] {
    font-size: 100px;
    position: absolute;
    left: 0;
    top: 0;
    opacity: 0;
  }

  .upload-content {
    position: inherit;
    top: 45%
  }

  .btn-rescale {
    position: absolute;
    color: #eeeeee;
    font-size: x-large;
    top: 5px;
    left: 15px;
    font-weight: 400;
  }

  .btn-pencil {
    position: absolute;
    color: #eeeeee;
    font-size: x-large;
    top: 5px;
    left: 40px;
    font-weight: 400;
  }

  img {
    height: auto;
    width: 100%;
  }

  .img-thumbnail-viewed {
    max-width: 50px;
    width: 50px;
    border: 3px dotted #dee2e6;
    height: auto;
  }

  .img-thumbnail-uploaded {
    max-width: 50px;
    width: 50px;
    border: 3px dotted #11e604;
    height: auto;
  }

  .img-thumbnail-uploading {
    max-width: 50px;
    width: 50px;
    border: 3px dotted #ffeb16;
    height: auto;
  }

  .navigation-arrow {
    font-size: 28px;
    background-color: #343a40
  }

  .navigation-arrow-hover:hover {
    cursor: pointer;
  }

  .flaticon2-back {
    color: white;
  }

  .flaticon2-next {
    color: white;
  }

</style>
