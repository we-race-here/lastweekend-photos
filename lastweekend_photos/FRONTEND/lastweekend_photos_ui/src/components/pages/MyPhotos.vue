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
                             placeholder="Select events..."></multiselect>
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
                      <a @click="removePhoto(photo)" class="btn btn-outline-danger btn-sm btn-icon btn-icon-md mr-1">
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
              :hide-footer="true">
        <div class="modal-body">
          <div class="row">
            <div class="col-6">
              <div class="row">
                <div class="kt-portlet">
                  <div class="kt-portlet__head">
                    <div class="kt-portlet__head-label">
                      <h5>{{Object.keys(uploadedPhotos).length}} photo(s) selected</h5>
                    </div>
                    <div class="kt-portlet__head-toolbar">
                      <div class="kt-portlet__head-actions">
                        <div class="upload-btn-wrapper">
                          <button class="btn btn-outline-brand btn-sm">Select photo(s)</button>
                          <input type="file" ref="selectedPhotosRef" @change="uploadFiles" multiple accept="image/*"/>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="kt-portlet__body">
                    <img :src="uploadedPhotos[uploadedPhotoPreviewName].address" v-if="uploadedPhotos[uploadedPhotoPreviewName]" class="size-auto"/>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-6">
              <div class="row ml-3">
                <div class="col">
                  <div class="row">
                    <div class="col">
                      <input type="text" class="form-control" id="uploadedPhotos[uploadedPhotoPreviewName].name"
                             placeholder="Pick a name for your photo">
                    </div>
                  </div>
                  <div class="row mt-2">
                    <div class="col">
                      <textarea aria-multiline="true" class="form-control"
                                id="uploadedPhotos[uploadedPhotoPreviewName].description"
                                placeholder="Add a description">
                      </textarea>
                    </div>
                  </div>
                  <div class="row mt-2">
                    <div class="col">
                      <input type="text" class="form-control" id="uploadedPhotos[uploadedPhotoPreviewName].price"
                             placeholder="Price">
                    </div>
                    <div class="col">
                      <div class="dropdown">
                        <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton"
                                data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                          Choose logo position {{logoPosition}}
                        </button>
                        <div class="dropdown-menu" aria-labelledby="dropdownMenuButton" x-placement="top-start"
                             style="position: absolute; will-change: transform; top: 0px; left: 0px; transform: translate3d(0px, -138px, 0px);">
                      <span class="dropdown-item" data-toggle="kt-tooltip" title="" data-placement="left"
                            @click="logoPosition='tl'"
                      >Top Left</span>
                          <span class="dropdown-item" data-toggle="kt-tooltip" title="" data-placement="left"
                                @click="logoPosition='tc'"
                          >Top Center</span>
                          <span class="dropdown-item" data-toggle="kt-tooltip" title="" data-placement="left"
                                @click="logoPosition='tr'"
                          >Top Right</span>
                          <span class="dropdown-item" data-toggle="kt-tooltip" title="" data-placement="left"
                                @click="logoPosition='cl'"
                          >Center Left</span>
                          <span class="dropdown-item" data-toggle="kt-tooltip" title="" data-placement="left"
                                @click="logoPosition='cc'"
                          >Center Center</span>
                          <span class="dropdown-item" data-toggle="kt-tooltip" title="" data-placement="left"
                                @click="logoPosition='cr'"
                          >Center Right</span>
                          <span class="dropdown-item" data-toggle="kt-tooltip" title="" data-placement="left"
                                @click="logoPosition='bl'"
                          >Bottom Left</span>
                          <span class="dropdown-item" data-toggle="kt-tooltip" title="" data-placement="left"
                                @click="logoPosition='bc'"
                          >Bottom Center</span>
                          <span class="dropdown-item" data-toggle="kt-tooltip" title="" data-placement="left"
                                @click="logoPosition='br'"
                          >Bottom Right</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="row mt-2">
                    <div class="col">
                      <input type="date" class="form-control" id="uploadedPhotos[uploadedPhotoPreviewName].date"
                             placeholder="when do you pick this photo?">
                    </div>
                  </div>
                  <div class="row">
                    <div class="col mt-2">
                      <multiselect v-model="selectedEvents" :options="events" :multiple="false" track-by="id"
                                   label="name"
                                   placeholder="Select events..."></multiselect>
                    </div>
                  </div>
                  <div class="row mt-2">
                    <div class="col">
                      <multiselect v-model="selectedTags" :options="tags" :multiple="true" track-by="id" label="name"
                                   placeholder="Select tags..."></multiselect>
                    </div>
                  </div>
                  <div class="row mt-2">
                    <div class="col">
                      <multiselect v-model="selectedPeople" :options="people" :multiple="true" track-by="id"
                                   label="name"
                                   placeholder="Select people..."></multiselect>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col">
              <b-container fluid class="p-4 bg-dark mt-2">
                <b-row>
                  <b-col v-for="index in 10" :key="(index - 1) + uploadedPhotoNavigationIndex">
                    <b-img thumbnail fluid
                           v-if="Object.keys(uploadedPhotos).length >= index + uploadedPhotoNavigationIndex"
                           :src="uploadedPhotos[Object.keys(uploadedPhotos)[(index - 1) + uploadedPhotoNavigationIndex]].address"
                           @click="uploadedPhotoPreviewName = Object.keys(uploadedPhotos)[(index - 1) + uploadedPhotoNavigationIndex]"></b-img>
                  </b-col>
                </b-row>
              </b-container>
            </div>
          </div>
          <div class="row">
            <div class="col">
              <button class="btn btn-success btn-block btn-lg mt-3 mr-3">
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
        <!-- /.modal-content -->
        <!-- /.modal-dialog -->
      </b-modal>

    </div>
  </section>
</template>

<script>
  import PageBar from "../partials/PageBar";
  import Multiselect from 'vue-multiselect'
  import UtilMixin from "../mixins/UtilMixin";
  import EventApi from "../../endpoint/EventApi";
  import PhotoApi from "../../endpoint/PhotoApi";
  import LogoPosition from "../model/LogoPosition"

  export default {
    name: "MyPhotos",
    components: {
      PageBar,
      Multiselect
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

      // Retrieve photo list
      this.getPhotos(this.searchValue, this.currentPage, this.pageSize);
    },
    watch: {
      "searchSelectedEvents": function () {
        this.getPhotos(this.searchSelectedEvents);
      },
      "searchValue": function () {
        // Debounce search request
        if (this.previousSearchTimeout) {
          clearTimeout(this.previousSearchTimeout);
        }
        this.previousSearchTimeout = setTimeout(() => {
          this.getPhotos(this.searchValue, this.currentPage, this.pageSize);
        }, 500)
      }
    },
    methods: {
      getPhotos: function (searchValue, currentPage, pageSize) {
        let params = {'search': searchValue, 'page': currentPage, 'page_size': pageSize};

        // Create events id
        if (this.selectedEvents.length > 0) {
          let ids = [];
          for (let i = 0; i < this.selectedEvents.length; i++) {
            ids.push(this.selectedEvents[i].id)
          }
          params['event'] = ids;
        }

        PhotoApi.getMine(params).then((resp) => {
          this.photos = resp.data;
        }, function () {

        })
      },
      openEditPhotoModal: function (photo) {
        this.selectedPhoto = photo;
        this.$refs.editPhotoModalRef.show();
      },
      uploadFiles: function () {

        for (let i = 0; i < this.$refs.selectedPhotosRef.files.length; i++) {
          let reader = new FileReader();
          let file = this.$refs.selectedPhotosRef.files[i];
          reader.onload = e => {
            let newPhoto = e.target.result;
            this.$set(this.uploadedPhotos, file.name, {address: newPhoto, uploaded: false});
          };
          reader.readAsDataURL(file);
        }
      },
    },
    data: function () {
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
        uploadedPhotos: {},
        uploadedPhotoPreviewName: 0,
        uploadedPhotoNavigationIndex: 0,
        selectedEvents: [],
        selectedTags: [],
        tags: [],
        selectedPeople: [],
        people: [],
        currentPage: 1,
        pageSize: 10
      }
    }
  }
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style scoped>

  #generalSearch {
    font-size: 1rem !important;
  }

  .multiselect__tags {
    min-height: 33px !important;
    height: 33px !important;;
    padding: 5px 40px 0 8px !important;;
    background-color: #F2F3F7 !important;
    border: 1px solid #ebedf2 !important;
    border-radius: 4px !important;
    display: flex !important;
    flex-shrink: 1 !important;
  }

  .multiselect__tag {
    background-color: #66cbfa !important;
  }

  .multiselect__input {
    background-color: #F2F3F7 !important;
  }

  .multiselect__select {
    top: 0 !important;
    padding: 0 !important;
  }

  .multiselect__placeholder {
    padding-top: 0 !important;
  }

  .multiselect__tags-wrap {
    display: flex;
    flex-flow: row nowrap;
    width: 100%;
  }

  .event-select {
    width: 70% !important;
    margin-top: 8px !important;
  }

  #kt_subheader_search_container .kt-subheader__main .kt-subheader__title {
    margin-top: 5px !important;
  }

  .modal .modal-content .modal-header .close:before {
    content: ""
  }

  .large-icon {
    font-size: 1.75rem;
  }

  .size-auto {
    width: 100%;
    height: auto;
  }

  .size-auto-1 {
    width: auto;
    height: auto;
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

</style>
