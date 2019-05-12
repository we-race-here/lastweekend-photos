<style>
  .kt-portlet__head {
    display: inline;
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

  .grey-gallery {
    background-color: #555555;
  }

  .no-padding {
    padding: 0px !important;
  }

  .active-image {
    border: 4px darkred solid;
  }

  .modal-full {
    height: 93%;
    display: flex;
    width: 100% !important;
    max-width: 100% !important;
    background-color: #555555;
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

  .upload-content{
    position: inherit;
    top:45%
  }

  .kt-portlet__head{
    display: block !important;
  }

</style>
<template>
  <div class="kt-portlet">
    <div class="kt-portlet__head mt-2">
      <span class="kt-menu__item" aria-haspopup="true">
        <span class="kt-menu__link-icon la la-plus-square-o h4"></span>
        <span class="kt-menu__link-text h5 mr-5"><a class="btn default" data-toggle="modal"
                                                         href="#add_photo_modal">
									Add photos</a></span>
      </span>
      <span class="kt-menu__item" aria-haspopup="true">
        <i class="kt-menu__link-icon la la-trash-o h4"></i><span
              class="kt-menu__link-text h5 mr-5">Remove selected</span>
      </span>
    </div>
    <div class="kt-portlet__body grey-gallery no-padding">
      <div class="row m-0">
        <div class="col-md-3 thumbnail">
          <input type="text" class="form-control" id="photo.name" placeholder="Pick a name for your photo">
          <hr>
          <textarea aria-multiline="true" class="form-control" id="photo.description" placeholder="add a description">
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
          <a href="#">or create a new group</a>
        </div>
        <div class="col-md-9">
          <div class="row">
            <div class="col-md-4 mt-3" v-for="(img, index) in images" v-bind:key="index">
              <img v-bind:src="'resources/images/'+img.address" @click="selectImage(img)"
                   v-bind:class="{'active-image':img.active}"
                   style="width: 100%;height: auto;">
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="modal fade" id="add_photo_modal" tabindex="-1" role="dialog" aria-hidden="true" style="display: none;">
      <div class="modal-dialog modal-full">
        <div class="modal-content">
          <div class="modal-body text-center">
            <div class="upload-content">
              <p>Drag & drop photos and videos here</p>
              <p>or</p>
              <div class="upload-btn-wrapper">
                <button class="btn-file">Upload a file</button>
                <input type="file" name="myfile"/>
              </div>
            </div>
          </div>
        </div>
        <!-- /.modal-content -->
      </div>
      <!-- /.modal-dialog -->
    </div>
  </div>

</template>

<script>
  export default {
    name: "MyPhotos",
    methods: {
      selectImage: function (thisImage) {
        let images = this.images;
        images.forEach(function (image) {
          if (image == thisImage) {
            image.active = true;
          } else {
            image.active = false;
          }

        })
      },
      isActive:

          function () {
            return Array.from(arguments).indexOf(this.$route.name) >= 0;
          }
    },
    data: function () {
      return {
        images: [{address: "img1.jpg", active: false}, {address: "img2.jpg", active: false}, {
          address: "img3.jpg",
          active: false
        }
          , {address: "img4.jpg", active: false}]
      }
    }
  }
</script>

<style scoped>

</style>