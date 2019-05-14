<template>
  <div class="kt-portlet">
    <div class="kt-portlet__head mt-2">
      <span class="kt-menu__item" aria-haspopup="true">
        <span class="kt-menu__link-icon la la-plus-square-o h4"></span>
        <span class="kt-menu__link-text h5 mr-5">
          <a class="btn default" @click="openFileModal">Add photos</a>
        </span>
      </span>
      <span class="kt-menu__item" aria-haspopup="true">
        <span class="kt-menu__link-icon la la-trash-o h4"></span>
        <span class="kt-menu__link-text h5 mr-5">
          <a class="btn default" @click="removeSelectedImages">Remove selected</a>
        </span>
      </span>
    </div>
    <div class="kt-portlet__body grey-gallery no-padding">
      <div class="row m-0">
        <div class="col-md-12">
          <div class="row">
            <div class="col-md-4 mt-3 mb-3" v-for="(img, index) in images" v-bind:key="index">
              <a @click="openFullscreenModal(index)"><span class="la la-arrows btn-rescale"></span></a>
              <a @click="openEditModal(index)"><span class="la la-pencil btn-pencil"></span></a>
              <img v-bind:src="img.address" @click="selectImage(img)"
                   v-bind:class="{'active-image':img.active}">
            </div>
          </div>
        </div>
      </div>
    </div>
    <modal class="modal fade" id="add_photo_modal" name="add_photo_modal" tabindex="-1" role="dialog" aria-hidden="true"
           style="display: none;">
      <div class="modal-dialog modal-full">
        <div class="modal-content">
          <div class="modal-body text-center" @drop="drop(event)" @dragover="allowDrop(event)">
            <div class="upload-content">
              <p>Drag & drop photos and videos here</p>
              <p>or</p>
              <div class="upload-btn-wrapper">
                <button class="btn-file">Upload a file</button>
                <input type="file" name="myfile" ref="newPhoto" @change="uploadFile"/>
              </div>
            </div>
          </div>
        </div>
        <!-- /.modal-content -->
      </div>
      <!-- /.modal-dialog -->
    </modal>

    <modal class="modal fade modal-scroll in" id="edit_modal" name="edit_modal" tabindex="-1" role="dialog"
           aria-hidden="true"
           style="display: none;">
      <div class="modal-dialog modal-scroll bg-white">
        <div class="modal-content">
          <div class="modal-body text-center">
            <img ref="editableImage" src="">
            <hr>
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
            <button class="btn btn-success">Save</button>
            &nbsp;
            <button class="btn btn-danger" @click="closeEditModal">Close</button>
          </div>
        </div>
        <!-- /.modal-content -->
      </div>
      <!-- /.modal-dialog -->
    </modal>

    <modal class="modal fade modal-scroll in" id="fullscreen_modal" name="fullscreen_modal" tabindex="-1" role="dialog"
           aria-hidden="true"
           style="display: none;">
      <div class="modal-dialog modal-full bg-white">
        <div class="modal-content">
          <div class="modal-body text-center">
            <img ref="fullscreenImage" src="">
          </div>
        </div>
      </div>
    </modal>
  </div>

</template>

<script>
    export default {
        name: "MyPhotos",
        methods: {
            drop: function () {
                alert('drop');
            },
            allowDrop: function (ev) {
                ev.preventDefault();
            },
            openFileModal: function () {
                $('#add_photo_modal').modal('show')
            },
            closeFileModal: function () {
                $('#add_photo_modal').modal('hide')
            },
            openEditModal: function (index) {
                this.$refs.editableImage.src = this.images[index].address;
                $('#edit_modal').modal('show')
            },
            closeEditModal: function () {
                $('#edit_modal').modal('hide')
            },
            openFullscreenModal: function (index) {
                this.$refs.fullscreenImage.src = this.images[index].address;
                $('#fullscreen_modal').modal('show')
            },
            closeFullscreenModal: function () {
                $('#fullscreen_modal').modal('hide')
            },
            removeSelectedImages: function () {
                let images = this.images;
                images.forEach(function (image, index) {
                    if (image.active == true) {
                        images.splice(index, 1);
                    }
                })
            },
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
            uploadFile: function () {
                let self = this;
                const reader = new FileReader();
                let file = this.$refs.newPhoto.files[0]
                let newImage;
                reader.onload = e => {
                    newImage = e.target.result;
                    self.images.push({address: newImage, active: false});
                    self.closeFileModal();
                }
                reader.readAsDataURL(file);
            },
            isActive: function () {
                    return Array.from(arguments).indexOf(this.$route.name) >= 0;
                }
        },
        data: function () {
            return {
                images: [{address: "resources/images/img1.jpg", active: false}, {
                    address: "resources/images/img2.jpg",
                    active: false
                }, {
                    address: "resources/images/img3.jpg",
                    active: false
                }
                    , {address: "resources/images/img4.jpg", active: false}]
            }
        }
    }
</script>

<style scoped>
  .kt-portlet__head {
    display: inline;
  }

  .grey-gallery {
    background-color: #ffffff;
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

  .kt-portlet__head {
    display: block !important;
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