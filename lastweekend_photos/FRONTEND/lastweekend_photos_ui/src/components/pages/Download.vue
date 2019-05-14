<template>
  <section>
    <div class="container">
      <div class="row">
        <div class="col-md-6">
          <div class="row">
            <div class="thumbnail">
              <div class="col-12 image-box">
                <img src='resources/images/img2.jpg'
                     style="width: 100%;height: auto;">
                <span class="cover-row">man in laps</span>
              </div>

              <div class="row h4">
                <div class="col-md-1 offset-2 h3">
                  <span class="la la-mail-forward"></span>
                </div>

                <div class="col-md-1 h3">
                  <span class="la la-star-o"></span>
                </div>

                <div class="col-md-1 h3">
                  <span class="la la-thumbs-o-up"></span>
                </div>

                <div class="col-md-2 text-center offset-2">
                  <span class="la la-comment-o"></span>
                  35
                </div>
                <div class="col-md-3 text-center">
                  <span class="la la-heart-o"></span>
                  443
                </div>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-md-2 text-center">
              <span class="la la-user h2"></span>
            </div>
            <div class="col-md-10">
              <div class="row">
                <div class="col-md-12 text-left h3 text-black">
                  albert nic
                </div>
              </div>
              <div class="row">
                <div class="col-md-12 text-left h3">
                  london
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="text-center">
            <ul class="nav nav-pills nav-fill" role="tablist">
              <li class="nav-item nav-small">
                <a class="nav-link active" data-toggle="tab" href="#small_size_tab">Small</a>
              </li>
              <li class="nav-item nav-medium">
                <a class="nav-link" data-toggle="tab" href="#medium_size_tab">Medium</a>
              </li>
              <li class="nav-item nav-large">
                <a class="nav-link" data-toggle="tab" href="#large_size_tab">Large</a>
              </li>
            </ul>
            <div class="tab-content">
              <div class="tab-pane active" id="small_size_tab" role="tabpanel">
                <div class="row mt-4">
                  <span class="border-bottom pb-4 btn-block text-black">Small | 1296 x 864 px | 43.9 x 29.3 cm @ 72 dpi | JPEG</span>
                </div>
                <div class="row mt-4">
                  <button class="btn btn-success btn-block btn-lg mt-2" @click="$refs.subscribePlanModalRef.show()">
                    Download original file
                  </button>
                </div>
                <div class="row mt-4">
                  <button class="btn btn-default btn-block btn-lg mt-2">Download for free (with Ads)</button>
                </div>
                <div class="row mt-4">
                  <button class="banner btn-block mt-2 btn-lg">ads banner</button>
                </div>
              </div>
              <div class="tab-pane" id="medium_size_tab" role="tabpanel">
                <p>Medium | 2592 x 1728 px | 43.9 x 29.3 cm @ 150 dpi | JPEG</p>
                <hr class="mt-2">
                <button class="btn btn-success btn-block btn-lg mt-2">Download original file</button>
                <button class="btn btn-default btn-block btn-lg mt-2">Download for free (with Ads)</button>
                <button class="banner btn-block mt-2 btn-lg">ads banner</button>
              </div>
              <div class="tab-pane" id="large_size_tab" role="tabpanel">
                <p>Large | 5184 x 3456 px | 43.9 x 29.3 cm @ 300 dpi | JPEG</p>
                <hr class="mt-2">
                <button class="btn btn-success btn-block btn-lg mt-2">Download original file</button>
                <button class="btn btn-default btn-block btn-lg mt-2">Download for free (with Ads)</button>
                <button class="banner btn-block mt-2 btn-lg">ads banner</button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="row mt-3">
        <div class="text-left container-fluid border-bottom pb-3">
          <h2 class="text-black">
            Happy male biker
          </h2>
        </div>
        <hr class="text-black">
        <div class="text-center container-fluid mt-3">
          <h3 class="text-black">
            Similar
          </h3>
        </div>
      </div>
      <div class="row">
        <div class="col-md-4 mt-2" v-for="(img, index) in images" v-bind:key="index">
          <img v-bind:src="img">
        </div>
      </div>
    </div>
    <b-modal
            centered
            ref="subscribePlanModalRef"
            id="subscribePlanModal"
            :hide-header="true"
    >
      <p class="h2">Ready to download?</p>
      <div class="modal-content">
        <div class="modal-body">
          <form>
            <div class="row">
              <div class="col">
                <span>It's simple. Your image will start downloading once you choose your plan. Our worry-free standard license covers the most common uses of his image.</span>
                <span class="font-weight-bold">Subscribe and save Annual plan, charged monthly.</span>
              </div>
            </div>
            <div class="row mt-3">
              <div class="col">
                <div class="kt-radio-list">
                  <label class="kt-radio">
                    <input type="radio" checked="checked" name="plan"> 10 images / month$29*
                    <span></span>
                    <h5>$2.90 per image</h5>
                  </label>
                  <label class="kt-radio">
                    <input type="radio" name="plan"> 350 images / month$169
                    <span></span>
                    <h5>$0.48 per image</h5>
                  </label>
                  <label class="kt-radio">
                    <input type="radio" name="plan"> just this image
                    <span></span>
                    <h5>$3 per image</h5>
                  </label>
                </div>
              </div>
            </div>

          </form>
        </div>
      </div>
      <div slot="modal-footer" class="w-100">
        <button
                type="button"
                class="btn btn-secondary float-left"
                @click="$refs.subscribePlanModalRef.hide()"
        >
          <i class="la la-close"></i> Cancel
        </button>
        <button
                type="button"
                class="btn btn-danger float-right">
          BUY AND DOWNLOAD
        </button>
      </div>
    </b-modal>
  </section>
</template>

<script>
    import bModal from "bootstrap-vue/es/components/modal/modal";

    export default {
        name: "Download",
        components: {
            "b-modal": bModal
        },
        data: function () {
            return {
                images: [
                    "resources/images/img1.jpg",
                    "resources/images/img4.jpg",
                    "resources/images/img2.jpg",
                    "resources/images/img3.jpg",
                    "resources/images/img2.jpg",
                    "resources/images/img4.jpg",
                ]
            }
        }
    }
</script>

<style scoped>
  .nav-small a {
    font-size: 14px !important;
  }

  .nav-medium a {
    font-size: 18px !important;
  }

  .nav-large a {
    font-size: 26px !important;
  }

  .banner {
    border: 1px solid #000000;
    background-color: #CCCCCC;
    border-radius: 5px;
    min-height: 100px;
  }
</style>