<style scoped>
.app-version-alert {
  border-radius: 0;
  font-size: 15px;
}
.refresh-btn {
  margin-left: 5px;
  margin-right: 5px;
  margin-top: -5px;
}
</style>

<template>
  <div class="fixed-bottom alert alert-danger kt-margin-0 app-version-alert">
    <i class="flaticon-warning kt-margin-r-5"></i> <span class="kt-font-boldest kt-margin-r-5"> Current ui version is old!</span>
    A new version of ui <span class="kt-badge kt-badge--primary kt-badge--inline kt-margin-l-5 kt-margin-r-5">{{ newVersion }}</span> is available.
    <a href="javascript:" onclick="location.reload()" class="btn btn-sm btn-warning refresh-btn">
      <i class="la la-refresh"></i> Click here
    </a> or refresh page to load new version.
  </div>
</template>

<script>
import UtilMixin from "../mixins/UtilMixin";

export default {
  props: {
    newVersion: {
      type: String,
      default: null
    }
  },
  mixins: [UtilMixin],
  mounted: function() {}
};
</script>
