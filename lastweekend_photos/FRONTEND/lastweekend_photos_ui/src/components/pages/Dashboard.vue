<template>
  <section>
    <page-bar></page-bar>
    <div class="kt-subheader kt-grid__item" id="kt_subheader_search_container">
      <div class="kt-subheader__main">
        <div class="container-fluid">
          <div class="row justify-content-md-center align-items-center">
            <div class="col-auto p-0">
              <h3 class="kt-subheader__title">
                Dashboard
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
    <div class="kt-portlet">
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
          <div class="col-6">
            <div class="row">
              <div class="kt-portlet">
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
                <div class="kt-portlet__body">
                  <img :src="selectedPhoto.preview_file" class="size-auto"/>
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
                         style="position: absolute; will-change: transform; top: 0px; left: 0px; transform: translate3d(0px, -138px, 0px);">
                      <a href="javascript:" v-for="p in logoPositionOptions" :key="p.value" class="dropdown-item"
                         :class="{active: p.value==(logoPosition || 'br')}"
                         data-toggle="kt-tooltip" data-placement="left" @click="logoPosition=p.value">
                        {{ p.title }}
                      </a>
                    </div>
                  </div>
                </div>
                <div class="row mt-4">
                  <button type="button" class="btn btn-secondary btn-block btn-lg mt-2" disabled>
                    Download original file
                  </button>
                </div>
                <div class="row mt-4">
                  <button type="button" @click="downloadWithLogoFile" class="btn btn-spinner btn-success btn-block btn-lg mt-2"
                          :disabled="selectedPhoto._downloadingWithAds">
                    <i :class="selectedPhoto._downloadingWithAds? 'la la-spin la-spinner':'flaticon2-download'"></i>
                    Free Download (with Ads)
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </b-modal>
  </section>
</template>

<script>
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
      downloadWithLogoFile: function() {
        var self = this;
        this.$set(this.selectedPhoto, '_downloadingWithAds', true);
        PhotoApi.getLowResFile(this.selectedPhoto, {ads_position: this.logoPosition}).then((resp) => {
          self.selectedPhoto.low_res_file = resp.data.file;
          self.download2(this.noCacheUrl(resp.data.file));
          self.$set(self.selectedPhoto, '_downloadingWithAds', false);
        }, function (error) {
          self.$set(self.selectedPhoto, '_downloadingWithAds', false);
          self.showDefaultServerError(error);
        })
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

<style scoped>

  .nav-link.active, .nav-link:hover {
    color: #000000 !important;
    border-color: #000000 !important;
  }

  .large-icon {
    font-size: 1.75rem;
  }

  .size-auto {
    width: 100%;
    height: auto;
  }

  .kt-subheader__main {
    width: 100%;
  }

  #generalSearch {
    font-size: 1rem !important;
  }

  .event-select {
    width: 70% !important;
    margin-top: 8px !important;
  }

</style>
