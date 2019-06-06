<template>
  <section>
    <page-bar></page-bar>
    <div class="kt-subheader kt-grid__item" id="kt_subheader_search_container">
      <div class="kt-subheader__main">
        <div class="container-fluid">
          <div class="row justify-content-md-center align-items-center">
            <div class="col-auto p-0">
              <h3 class="kt-subheader__title">
                My Photos
              </h3>
            </div>
            <div class="col-auto mt-1 p-0">
              <span class="kt-subheader__separator kt-subheader__separator--v"></span>
            </div>
            <div class="col-auto mt-1 p-0">
              <span class="kt-subheader__desc" id="kt_subheader_total">{{photos.pagination.total}} Total</span>
            </div>
            <div class="col-md-6 col-sm-12 p-0 mr-auto kt-subheader__group" id="kt_subheader_search">
              <div class="kt-input-icon kt-input-icon--right kt-subheader__search mr-3">
                <input type="text" class="form-control" placeholder="Search..." id="generalSearch"
                       v-model="searchValue">
                <span class="kt-input-icon__icon kt-input-icon__icon--right">
                            <span>
                                <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
                                     width="24px" height="24px" viewBox="0 0 24 24" version="1.1" class="kt-svg-icon">
    <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
        <rect id="bound" x="0" y="0" width="24" height="24"></rect>
        <path d="M14.2928932,16.7071068 C13.9023689,16.3165825 13.9023689,15.6834175 14.2928932,15.2928932 C14.6834175,14.9023689 15.3165825,14.9023689 15.7071068,15.2928932 L19.7071068,19.2928932 C20.0976311,19.6834175 20.0976311,20.3165825 19.7071068,20.7071068 C19.3165825,21.0976311 18.6834175,21.0976311 18.2928932,20.7071068 L14.2928932,16.7071068 Z"
              id="Path-2" fill="#000000" fill-rule="nonzero" opacity="0.3"></path>
        <path d="M11,16 C13.7614237,16 16,13.7614237 16,11 C16,8.23857625 13.7614237,6 11,6 C8.23857625,6 6,8.23857625 6,11 C6,13.7614237 8.23857625,16 11,16 Z M11,18 C7.13400675,18 4,14.8659932 4,11 C4,7.13400675 7.13400675,4 11,4 C14.8659932,4 18,7.13400675 18,11 C18,14.8659932 14.8659932,18 11,18 Z"
              id="Path" fill="#000000" fill-rule="nonzero"></path>
    </g>
</svg>                                <!--<i class="flaticon2-search-1"></i>-->
                            </span>
                        </span>
              </div>
              <div class="kt-subheader__search event-select">
                <multiselect v-model="searchSelectedEvents" :options="events" :multiple="true" track-by="id"
                             label="name"
                             placeholder="Select events...">
                </multiselect>
              </div>
            </div>
            <div class="col-md-auto col-sm-12 p-0">
              <a class="btn btn-outline-brand btn-sm" @click="$refs.addPhotoModalRef.show()">
                Add photo
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="kt-portlet">
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
                      <a @click="openEditPhotoModal(photo)"
                         class="btn btn-outline-success btn-sm btn-icon btn-icon-md mr-1">
                        <i class="flaticon-edit"></i>
                      </a>
                      <a @click="showConfirmDeleteModal(photo)"
                         class="btn btn-outline-danger btn-sm btn-icon btn-icon-md mr-1">
                        <i class="flaticon-delete"></i>
                      </a>
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
                            @input="getPhotos(searchValue, currentPage, pageSize)">
              </b-pagination>
            </div>
          </div>
        </div>
      </div>

      <!-- Add photo modal -->
      <b-modal
              size="lg"
              centered
              ref="addPhotoModalRef"
              id="addPhotoModal"
              title="Add new photo"
              @hide="onAddPhotoModalHide"
              :hide-footer="true">
        <div class="modal-body">
          <div class="row">
            <div class="col-md-6 col-sm-12">
              <div class="row">
                <div class="kt-portlet">
                  <div class="kt-portlet__head">
                    <div class="kt-portlet__head-label">
                      <h5>{{selectedPhotos[0].name === unknownFileName ? 0 : selectedPhotos.length}} photo(s)
                        selected</h5>
                    </div>
                    <div class="kt-portlet__head-toolbar">
                      <div class="kt-portlet__head-actions">
                        <div class="upload-btn-wrapper">
                          <button class="btn btn-outline-brand btn-sm">Select photo(s)
                          </button>
                          <input type="file" ref="selectedPhotosRef" @change="selectPhotos" multiple accept="image/*"/>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="kt-portlet__body">
                    <img :src="selectedPhotos[selectedPhotoIndex].original_file"
                         v-if="selectedPhotos[selectedPhotoIndex]" class="size-auto-fix"/>
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
                          Choose logo position {{selectedPhotos[selectedPhotoIndex].logo_position}}
                        </button>
                        <div class="dropdown-menu" aria-labelledby="dropdownMenuButton" x-placement="top-start"
                             style="position: absolute; will-change: transform; top: 0px; left: 0px; transform: translate3d(0px, -138px, 0px);">
                      <span class="dropdown-item" data-toggle="kt-tooltip" title="" data-placement="left"
                            @click="selectedPhotos[selectedPhotoIndex].logo_position='tl'"
                      >Top Left</span>
                          <span class="dropdown-item" data-toggle="kt-tooltip" title="" data-placement="left"
                                @click="selectedPhotos[selectedPhotoIndex].logo_position='tc'"
                          >Top Center</span>
                          <span class="dropdown-item" data-toggle="kt-tooltip" title="" data-placement="left"
                                @click="selectedPhotos[selectedPhotoIndex].logo_position='tr'"
                          >Top Right</span>
                          <span class="dropdown-item" data-toggle="kt-tooltip" title="" data-placement="left"
                                @click="selectedPhotos[selectedPhotoIndex].logo_position='cl'"
                          >Center Left</span>
                          <span class="dropdown-item" data-toggle="kt-tooltip" title="" data-placement="left"
                                @click="selectedPhotos[selectedPhotoIndex].logo_position='cc'"
                          >Center Center</span>
                          <span class="dropdown-item" data-toggle="kt-tooltip" title="" data-placement="left"
                                @click="selectedPhotos[selectedPhotoIndex].logo_position='cr'"
                          >Center Right</span>
                          <span class="dropdown-item" data-toggle="kt-tooltip" title="" data-placement="left"
                                @click="selectedPhotos[selectedPhotoIndex].logo_position='bl'"
                          >Bottom Left</span>
                          <span class="dropdown-item" data-toggle="kt-tooltip" title="" data-placement="left"
                                @click="selectedPhotos[selectedPhotoIndex].logo_position='bc'"
                          >Bottom Center</span>
                          <span class="dropdown-item" data-toggle="kt-tooltip" title="" data-placement="left"
                                @click="selectedPhotos[selectedPhotoIndex].logo_position='br'"
                          >Bottom Right</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="row mt-2">
                    <div class="col">
                      <dateTime placeholder="when do you pick this photo?"
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
          <div class="row mt-2" v-if="selectedPhotos[0].name !== unknownFileName">
            <div class="col-auto navigation-arrow d-flex align-items-center"
                 :class="{'navigation-arrow-hover': selectedPhotoIndex > 0}" @click="previousPhoto">
              <i class="flaticon2-back"></i>
            </div>
            <div class="col p-0">
              <b-container fluid class="p-4 bg-dark">
                <b-row>
                  <b-col v-for="index in 10" :key="(index - 1) + selectedPhotoNavigationIndex">
                    <b-img fluid
                           v-bind:class="selectedPhotos[(index - 1) + selectedPhotoNavigationIndex].uploaded ? 'img-thumbnail-uploaded' : (selectedPhotoIndex === (index - 1) + selectedPhotoNavigationIndex ? 'img-thumbnail-viewed' : '')"
                           v-if="selectedPhotos.length >= index + selectedPhotoNavigationIndex"
                           :src="selectedPhotos[(index - 1) + selectedPhotoNavigationIndex].original_file"
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
              <button class="btn btn-success btn-block btn-lg mt-3 mr-3" @click="uploadPhotos">
                Upload
              </button>
            </div>
          </div>
        </div>
      </b-modal>

      <!-- Edit modal -->
      <b-modal
              size="md"
              centered
              ref="editPhotoModalRef"
              id="editPhotoModal"
              :title="'Edit ' + selectedPhoto.title"
              :hide-footer="true">
        <div class="modal-body text-center">
          <img ref="editableImage" :src="selectedPhoto.preview_file">
          <hr>
          <input type="text" class="form-control" id="photo.name" placeholder="Pick a name for your photo">
          <hr>
          <textarea aria-multiline="true" class="form-control" id="photo.description"
                    placeholder="add a description">
          </textarea>
          <hr>
          <input type="text" class="form-control" id="photo.tag" placeholder="add some tag and press enter">
          <hr>
          <input type="text" class="form-control" id="photo.people" placeholder="add people by name or ID or email">
          <hr>
          <span>add to album</span>
          <div>
            <select class="form-control">
              <option>
                choose your album
              </option>
              <option>
                album 1
              </option>
              <option>
                album 2
              </option>
            </select>
          </div>
          <div class="text-left">
            <a href="#">or create a new group</a>
          </div>
          <hr>
          <span>add to group</span>
          <div>
            <select class="form-control">
              <option>
                choose your group
              </option>
              <option>
                album 1
              </option>
              <option>
                album 2
              </option>
            </select>
          </div>
          <div class="text-left">
            <a href="#">or create a new group</a>
          </div>
          <button class="btn btn-success">Save</button>&nbsp;
          <button class="btn btn-danger" @click="$refs.editPhotoModalRef.hide()">Close</button>
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
  </section>
</template>

<script>
  import PageBar from "../partials/PageBar";
  import Multiselect from 'vue-multiselect'
  import UtilMixin from "../mixins/UtilMixin";
  import EventApi from "../../endpoint/EventApi";
  import TagApi from "../../endpoint/TagApi";
  import PeopleApi from "../../endpoint/PeopleApi";
  import PhotoApi from "../../endpoint/PhotoApi";
  import LogoPosition from "../model/LogoPosition"
  import dateTime from "../libs/VueDatetimepicker";

  export default {
    name: "MyPhotos",
    components: {
      PageBar,
      Multiselect,
      dateTime
    },
    mixins: [
      UtilMixin
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
    methods: {
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

        PhotoApi.getMine(params).then((resp) => {
          this.photos = resp.data;
        }, (resp) => {
          this.showMessage((resp.response && resp.response.data.detail) ||
              "Some error happened when trying to get my photo")
        })
      },
      openEditPhotoModal: function (photo) {
        this.selectedPhoto = photo;
        this.$refs.editPhotoModalRef.show();
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
              continue;
            }
          }
          if (isDuplicate) {
            continue;
          }

          reader.onload = e => {
            let newPhoto = e.target.result;
            this.selectedPhotos.push({
              name: file.name,
              original_file: newPhoto,
              _event: {
                name: "Select a event..."
              },
              _tags: [],
              _peoples: [],
              uploaded: false
            });

            if (this.selectedPhotos.length > 1 &&
                this.selectedPhotos[0].name === this.unknownFileName) {
              this.selectedPhotos.splice(0, 1);
            }
          };
          reader.readAsDataURL(file);
        }
        this.$refs.selectedPhotosRef.value = "";
      },
      uploadPhotos: function () {
        if (this.selectedPhotos[0].name === this.unknownFileName) {
          this.showError("No photo selected");
          return;
        }

        for (let i = 0; i < this.selectedPhotos.length; i++) {
          let uploadPhoto = this.selectedPhotos[i];
          if (uploadPhoto.uploaded) {
            continue;
          }
          // Each photo only correspond to one event
          uploadPhoto.event = uploadPhoto._event.id;

          uploadPhoto.tags = [];
          for (let j = 0; j < uploadPhoto._tags.length; j++) {
            uploadPhoto.tags.push(uploadPhoto._tags[j].id);
          }

          uploadPhoto.peoples = [];
          for (let j = 0; j < uploadPhoto._peoples.length; j++) {
            uploadPhoto.peoples.push(uploadPhoto._peoples[j].id);
          }

          uploadPhoto.uploading = true;
          PhotoApi.upload(uploadPhoto).then(() => {
                uploadPhoto.uploading = false;
                uploadPhoto.uploaded = true;
                this.showSuccess(`The ${uploadPhoto.name} photo upload successfully`, 500);
              }, () => {
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
      onAddPhotoModalHide: function () {
        this.selectedPhotos = [
          {
            name: this.unknownFileName,
          }
        ];
        this.selectedPhotoIndex = 0;
        this.selectedPhotoNavigationIndex = 0;
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
      }
    },
    data: function () {
      const unknownFileName = "__unknown__";
      return {
        searchValue: "",
        logoPosition: "",
        previousSearchTimeout: LogoPosition.BottomRight,
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
        deletingPhoto: false
      }
    }
  }
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

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
    height: auto;
  }

  .size-auto-fix {
    width: 320px;
    height: 300px;
  }

  .kt-subheader__main {
    width: 100%;
  }

  .no-padding {
    padding: 0px !important;
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

  .navigation-arrow {
    font-size: 28px;
    background-color: #343a40
  }

  .navigation-arrow-hover:hover {
    cursor: pointer;
  }

</style>
