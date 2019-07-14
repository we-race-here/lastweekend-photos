<style scoped>
  .kt-subheader {
    margin-left: -25px;
    margin-right: -25px;
    background-color: #fff;
    padding-bottom: 10px;
    padding-top: 10px;
    padding-left: 25px;
    margin-top: 2px;
    margin-bottom: 15px;
  }
</style>

<template>
  <div class="kt-subheader kt-grid__item" id="kt_subheader">
    <div class="kt-subheader__main">
      <slot name="pre-title"></slot>
      <slot name="title">
        <h3 class="kt-subheader__title">
          {{$route.meta.pageInfo.title}}
        </h3>
        <span class="kt-subheader__separator kt-subheader__separator--v"></span>
      </slot>
      <slot name="post-title"></slot>
      <slot name="breadcrumb">
        <div class="kt-subheader__breadcrumbs">
          <slot name="breadcrumb-items">
            <a is="router-link" :to="{name: $rns.ROOT}" class="kt-subheader__breadcrumbs-home">
              <i class="fas fa-home"></i>
            </a>
            <template v-if="$route.meta.pageInfo.back">
              <span class="kt-subheader__breadcrumbs-separator"></span>
              <a is="router-link" :to="{name: $route.meta.pageInfo.back}"  class="kt-subheader__breadcrumbs-link">
                {{$router.resolve({name: $route.meta.pageInfo.back}).resolved.meta.pageInfo.title}}
              </a>
            </template>
            <span class="kt-subheader__breadcrumbs-separator"></span>
            <slot name="breadcrumb-title">
            <a class="kt-subheader__breadcrumbs-link--active">
              <slot name="breadcrumb-title-text">
              {{$route.meta.pageInfo.title}}
              </slot>
            </a>
            </slot>
          </slot>
        </div>
      </slot>

    </div>
    <slot name="action-section">
    <div class="kt-subheader__toolbar">
      <div class="kt-subheader__wrapper">
        <slot name="action-section-items">
        </slot>
      </div>
    </div>
    </slot>
  </div>
</template>
