<style scoped>
  .low-res-photo-not-loaded {
    opacity: 0.4;
  }

  .nav-link.active, .nav-link:hover {
    color: #000000 !important;
    border-color: #000000 !important;
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

  .sponsor-size-auto {
    width: 70px;
    height: 65px;
    object-fit: cover;
    border: 2px solid #6986e9;
    border-radius: 4px;
  }

  .overflow {
    width: 5em;
    text-overflow: ellipsis;
    /**
     * Required properties to achieve text-overflow
     */
    white-space: nowrap;
    overflow: hidden;
  }

  #kt_subheader_search_container {
    width: 100%;
  }

  #generalSearch {
    font-size: 1rem !important;
  }

  .event-select {
    width: 70% !important;
    margin-top: 8px !important;
  }

  .overlay {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    height: 100%;
    width: 100%;
    opacity: 0.7;
    transition: .5s ease;
    background-color: gray;
  }

  .overlay-loader {
    position: absolute;
    top: 50%;
    left: 50%;
    color: white;
  }


</style>

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
                    <multiselect v-model="selectedEvents" :options="events" :multiple="true" track-by="id" label="name"
                                 placeholder="Select events..."></multiselect>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>
      <div class="kt-portlet__body">
        <div class="container-fluid mr-3 ml-3">
          <div class="row">
            <div class="col-md-4 mt-3 mb-3" v-for="photo in photos.results" :key="photo.id">
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
                      <button type="button" @click="openDownloadPhotoModal(photo)"
                              class="btn btn-outline-success btn-sm btn-icon btn-icon-md mr-1">
                        <i class="flaticon-download"></i>
                      </button>
                      <a href="javascript:" class="btn btn-outline-danger btn-sm btn-icon btn-icon-md mr-1">
                        <i class="flaticon-star"></i>
                      </a>
                    </div>
                  </div>
                </div>
                <div class="kt-portlet__body">
                  <img :src="photo.preview_file" class="size-auto"/>
                </div>
                <div class="kt-portlet__foot kt-portlet__foot--sm kt-align-right">
                  <div class="d-flex">
                    <div v-for="sponsor in photo._event._sponsors" :key="sponsor.id" class="mr-2 d-flex flex-column">
                      <img :src="sponsor.logo" class="sponsor-size-auto">
                      <span class="overflow">{{sponsor.brand_name}}</span>
                    </div>
                  </div>

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
    </div>
    <!-- download modal -->
    <b-modal
            size="lg"
            centered
            ref="downloadModalModalRef"
            id="downloadModal"
            :title="'Ready to download ' + selectedPhoto.title + '?'"
            :hide-footer="true"
    >
      <div class="modal-body">
        <div class="row">
          <div class="col-7">
            <div class="row">
              <div class="kt-portlet kt-portlet--bordered">
                <div class="kt-portlet__head">
                  <div class="kt-portlet__head-label">
                              <span class="kt-portlet__head-icon">
                                <i class="la la-user large-icon"></i>
                              </span>
                    <h3 class="kt-portlet__head-title">
                      {{selectedPhoto.title}}
                    </h3>
                  </div>
                </div>
                <div class="kt-portlet__body kt-padding-10"
                     :class="{'low-res-photo-not-loaded': !selectedPhoto.low_res_file}">
                  <img :src="selectedPhoto.low_res_file || selectedPhoto.preview_file" class="size-auto"/>
                  <div class="overlay" v-if="selectedPhoto._gettingLowResFile">
                    <div class="overlay-loader"><i class="fa fa-spin fa-spinner fa-2x"></i></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-5">
            <div class="row ml-3">
              <div class="col">
                <div class="row">
                  <div class="dropdown">
                    <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton"
                            data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                      Logo position:
                      <span class="kt-font-bolder">{{ logoPositionMap[logoPosition || 'br'].title }}</span>
                    </button>
                    <div class="dropdown-menu" aria-labelledby="dropdownMenuButton" x-placement="top-start"
                         style="position: absolute; will-change: transform; top: 0; left: 0; transform: translate3d(0, -138px, 0);">
                      <a href="javascript:" v-for="p in logoPositionOptions" :key="p.value" class="dropdown-item"
                         :class="{active: p.value==(logoPosition || 'br')}"
                         data-toggle="kt-tooltip" data-placement="left"
                         @click="logoPosition=p.value; selectedPhoto.low_res_file=null">
                        {{ p.title }}
                      </a>
                    </div>
                  </div>
                </div>
                <div class="row mt-2">
                  <button type="button" class="btn btn-secondary btn-block btn-lg" disabled>
                    <i class="flaticon2-download"></i>
                    Download original file
                  </button>
                </div>
                <div v-if="!selectedPhoto.low_res_file" class="row mt-2">
                  <button type="button" @click="getLowResPhotoLink" class="btn btn-spinner btn-primary btn-block btn-lg"
                          :disabled="selectedPhoto._gettingLowResFile || selectedPhoto.low_res_file">
                    <i :class="selectedPhoto._gettingLowResFile? 'la la-spin la-spinner':'la la-link'"></i>
                    Get Photo Link(With Ads)
                  </button>
                </div>
                <template v-else>
                  <hr>
                  <div class="row mb-2">
                    <button type="button" @click="downloadLowResPhoto" class="btn btn-spinner btn-success btn-block">
                      <i class="flaticon2-download"></i>
                      Download Photo(With Ads)
                    </button>
                  </div>
                  <social-sharing :url="selectedPhoto.low_res_file"
                                  :title="selectedPhoto.title || 'N/A'"
                                  :description="selectedPhoto.description || 'N/A'"
                                  hashtags="weracehere,wrhphoto"
                                  v-cloak inline-template>
                    <div class="row">
                      <network network="facebook" id="facebook">
                        <button type="button" class="btn btn-facebook btn-square">
                          <i class="socicon-facebook"></i>
                          Facebook Share
                        </button>
                      </network>
                      <network network="twitter" id="twitter">
                        <button type="button" class="btn btn btn-twitter btn-square">
                          <i class="socicon-twitter"></i>
                          Twitter Share
                        </button>
                      </network>
                    </div>
                  </social-sharing>
                  <div class="row mt-2">
                    <div class="input-group input-group-sm">
                      <div class="input-group-prepend">
                        <span class="input-group-text">
                          Link:
                        </span>
                      </div>
                      <input id="photo-link-for-clipboard" v-model="selectedPhoto.low_res_file" type="text"
                             @click="selectPhotoLink()"
                             class="form-control" title="Photo link" readonly>
                      <div class="input-group-append" @click="copyPhotoLinkToClipboard()">
                        <span class="input-group-text pointer-cursor">
                          <i class="flaticon2-copy" title="Copy photo link to clipboard"></i>
                        </span>
                      </div>
                    </div>
                  </div>
                </template>
              </div>
            </div>
          </div>
        </div>
      </div>
    </b-modal>
  </div>
</template>

<script>
  import SocialSharing from "vue-social-sharing";

  import PageBar from "../partials/PageBar";
  import EventApi from "../../endpoint/EventApi";
  import PhotoApi from "../../endpoint/PhotoApi";
  import Multiselect from 'vue-multiselect'
  import UtilMixin from "../mixins/UtilMixin";
  import LoadingOverlayableMixin from "../mixins/LoadingOverlayableMixin";
  import LogoPosition from "../model/LogoPosition"
  import {
    LOGO_POSITION_OPTIONS, LOGO_POSITION_MAP
  } from "../../Constants";

  export default {
    components: {
      PageBar,
      Multiselect,
      SocialSharing
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

      // Retrieve photo list
      this.getPhotos(this.searchValue, this.currentPage, this.pageSize);
    },
    data: function () {
      return {
        logoPositionOptions: LOGO_POSITION_OPTIONS,
        logoPositionMap: LOGO_POSITION_MAP,
        searchValue: "",
        logoPosition: "",
        previousSearchTimeout: LogoPosition.BottomRight,
        selectedPhoto: {},
        photos: {
          pagination: {},
          results: []
        },
        selectedEvents: [],
        events: [],
        currentPage: 1,
        pageSize: 9
      }
    },
    watch: {
      "selectedEvents": function () {
        this.getPhotos(this.selectedEvents);
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
      selectPhotoLink: function () {
        var copyText = document.getElementById("photo-link-for-clipboard");
        copyText.select();
      },
      copyPhotoLinkToClipboard: function () {
        this.selectPhotoLink();
        document.execCommand("copy");
      },
      getLowResPhotoLink: function () {
        var self = this;
        this.$set(this.selectedPhoto, '_gettingLowResFile', true);
        PhotoApi.getLowResFile(this.selectedPhoto, {ads_position: this.logoPosition}).then((resp) => {
          self.selectedPhoto.low_res_file = resp.data.file;
          self.$set(self.selectedPhoto, '_gettingLowResFile', false);
        }, function (error) {
          self.$set(self.selectedPhoto, '_gettingLowResFile', false);
          self.showDefaultServerError(error);
        })
      },
      downloadLowResPhoto: function () {
        if (!this.selectedPhoto.low_res_file) {
          return;
        }
        this.download2(this.selectedPhoto.low_res_file);
      },
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
        this.loadingOverlay = true;
        PhotoApi.getAll(params).then((resp) => {
          this.loadingOverlay = false;
          this.photos = resp.data;
        }, (resp) => {
          this.loadingOverlay = false;
        })
      },
      openDownloadPhotoModal: function (photo) {
        this.selectedPhoto = photo;
        this.$refs.downloadModalModalRef.show();
      }
    }
  }
</script>
