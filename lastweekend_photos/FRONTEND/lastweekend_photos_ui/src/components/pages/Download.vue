<style>
  .text-black {
    color: #000000;
  }


  .cover-row {
    position: absolute;
    width: 96%;
    z-index: 2;
    opacity: 0.8;
    color: #000000;
    background-color: #cccccc;
    bottom: 0px;
    margin-left: 10px;
    left: 0px;
  }

  .la {
    cursor: pointer;
  }

  .thumbnail {
    padding: 4px;
    line-height: 1.42857;
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 4px;
    -webkit-transition: border .2s ease-in-out;
    -o-transition: border .2s ease-in-out;
    transition: border .2s ease-in-out;
  }

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
<template>
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
                <button class="btn btn-success btn-block btn-lg mt-2">Download original file</button>
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
      <div class="col-md-4 mt-2" v-for="img in images" v-bind:key="img">
        <img v-bind:src="img">
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "Download",
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

</style>