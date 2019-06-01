<template>
  <section>
    <page-bar></page-bar>
    <div class="kt-subheader   kt-grid__item" id="kt_subheader">
      <div class="kt-subheader__main">

        <h3 class="kt-subheader__title">
          Photos
        </h3>

        <span class="kt-subheader__separator kt-subheader__separator--v"></span>

        <div class="kt-subheader__group" id="kt_subheader_search">
          <span class="kt-subheader__desc" id="kt_subheader_total">{{photos.length}} Total</span>
          <div class="kt-input-icon kt-input-icon--right kt-subheader__search mr-3">
            <input type="text" class="form-control" placeholder="Search..." id="generalSearch" v-model="searchValue">
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
            <multiselect v-model="selectedEvents" :options="events" :multiple="true" track-by="id" label="name"
                         placeholder="Select events..."></multiselect>
          </div>
        </div>
      </div>
    </div>
    <div class="kt-portlet">
      <div class="kt-portlet__body">
        <ul class="nav nav-tabs nav-tabs-line nav-tabs-line-brand nav-tabs-line-2x nav-tabs-line-right nav-tabs-bold text-center"
            role="tablist">
          <li class="nav-item">
            <a class="nav-link active" data-toggle="tab" href="#all_activity_tab_content"
               role="tab">
              All Activity
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link" data-toggle="tab" href="#friends_tab_content" role="tab">
              Friends
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link" data-toggle="tab" href="#groups_tab_content" role="tab">
              Groups
            </a>
          </li>
        </ul>
        <div class="tab-content">
          <div class="tab-pane active" id="all_activity_tab_content" role="tabpanel">
            <form class="kt-form kt-form--label-right">
              <div class="kt-section kt-section--first">
                <div class="kt-section__body">
                  <div class="form-group kt-form__group row">
                    <div class="container-fluid mr-3 ml-3">
                      <div class="row">
                        <div class="col-md-4" v-for="photo in photos" :key="photo.id">
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
                                  <a href="#" class="btn btn-outline-success btn-sm btn-icon btn-icon-md mr-1">
                                    <i class="flaticon-download"></i>
                                  </a>
                                  <a href="#" class="btn btn-outline-danger btn-sm btn-icon btn-icon-md mr-1">
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
                    </div>
                  </div>
                </div>
              </div>
            </form>
          </div>
          <div class="tab-pane active" id="friends_tab_content" role="tabpanel">
            <form class="kt-form kt-form--label-right">
              <div class="kt-section kt-section--first">
                <div class="kt-section__body">
                  <div class="form-group kt-form__group row">
                  </div>
                </div>
              </div>
            </form>
          </div>
          <div class="tab-pane active" id="groups_tab_content" role="tabpanel">
            <form class="kt-form kt-form--label-right">
              <div class="kt-section kt-section--first">
                <div class="kt-section__body">
                  <div class="form-group kt-form__group row">
                  </div>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
  import PageBar from "../partials/PageBar";
  import EventApi from "../../endpoint/EventApi";
  import PhotoApi from "../../endpoint/PhotoApi";
  import Multiselect from 'vue-multiselect'
  import UtilMixin from "../mixins/UtilMixin";

  export default {
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
      this.getPhotos();
    },
    data: function () {
      return {
        searchValue: "",
        previousSearchTimeout: undefined,
        photos: [],
        selectedEvents: [],
        events: []
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
          this.getPhotos();
        }, 500)
      }
    },
    methods: {
      getPhotos: function () {
        let params = {'search': this.searchValue};

        // Create events id
        if (this.selectedEvents.length > 0) {
          let ids = [];
          for (let i = 0; i < this.selectedEvents.length; i++) {
            ids.push(this.selectedEvents[i].id)
          }
          params['event'] = ids;
        }

        PhotoApi.get(params).then((resp) => {
          this.photos = resp.data.results;
        }, function () {

        })
      }
    }
  }
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style>

  .element-box {
    margin-left: 4.444%
  }

  .nav-link.active, .nav-link:hover {
    color: #000000 !important;
    border-color: #000000 !important;
  }

  .nav-tabs.nav-tabs-line.nav-tabs-line-brand.nav-tabs-line-2x {
    border: none !important;;
  }

  .large {
    width: 80%;
  }

  .large-icon {
    font-size: 1.75rem;
  }

  .size-auto {
    width: auto;
    height: auto;
  }

  .kt-subheader__main {
    width: 100%;
  }

  #generalSearch {
    font-size: 1rem !important;
  }

  #kt_subheader_search {
    display: flex;
    flex-flow: row wrap;
    align-items: center;
    width: 80%;
    margin-top: 8px;
  }

  .multiselect__tags {
    min-height: 33px !important;
    height: 33px !important;;
    padding: 5px 40px 0 8px !important;;
    background-color: #F2F3F7 !important;
    border: 1px solid #ebedf2 !important;
    border-radius: 4px !important;
    display: flex !important;
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
    width: 50% !important;
    margin-top: 8px !important;
  }

  #kt_subheader .kt-subheader__title {
    margin-top: 5px !important;
  }

</style>
