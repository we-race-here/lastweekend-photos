<style scoped>

</style>

<template>
  <div>
    <page-bar></page-bar>
    <div class="kt-portlet">
      <div class="kt-portlet__head">
				<div class="kt-portlet__head-label">
					<span class="kt-portlet__head-icon kt-hide">
						<i class="la la-gear"></i>
					</span>
					<h3 class="kt-portlet__head-title">
						Dashboard
					</h3>
				</div>
			</div>
      <div class="kt-portlet__body">
        <div class="kt-section">
					<div class="kt-section__info">
						the statistics info and summary can be shown here.
					</div>
					<div class="kt-section__content">
            <h3>Not Implemented Yet!</h3>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import PageBar from "../partials/PageBar";
  export default {
    components: { PageBar }
  }
</script>
