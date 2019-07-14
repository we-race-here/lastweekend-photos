<template>
  <div class="kt-grid kt-grid--hor kt-grid--root">
		<div id="kt_header_mobile" class="kt-header-mobile  kt-header-mobile--fixed ">
			<div class="kt-header-mobile__logo">
				<a href="index.html">
					<img alt="Logo" :src="`${$publicPath}resources/images/logo-6-sm.png`" />
				</a>
			</div>
			<div class="kt-header-mobile__toolbar">
				<div class="kt-header-mobile__toolbar-toggler kt-header-mobile__toolbar-toggler--left" id="kt_aside_mobile_toggler"><span></span></div>
				<div class="kt-header-mobile__toolbar-toggler" id="kt_header_mobile_toggler"><span></span></div>
				<div class="kt-header-mobile__toolbar-topbar-toggler" id="kt_header_mobile_topbar_toggler"><i class="flaticon-more"></i></div>
			</div>
		</div>

		<div class="kt-grid kt-grid--hor kt-grid--root">
			<div class="kt-grid__item kt-grid__item--fluid kt-grid kt-grid--ver kt-page">
				<button class="kt-aside-close " id="kt_aside_close_btn"><i class="la la-close"></i></button>
        <side-menu></side-menu>
				<div class="kt-grid__item kt-grid__item--fluid kt-grid kt-grid--hor kt-wrapper" id="kt_wrapper">
          <main-header></main-header>
					<div class="kt-grid__item kt-grid__item--fluid kt-grid kt-grid--hor">
            <div class="kt-container  kt-container--fluid  kt-grid__item kt-grid__item--fluid">
              <keep-alive include="EventList">
                <router-view></router-view>
              </keep-alive>
            </div>
					</div>

					<main-footer></main-footer>
				</div>
			</div>
		</div>
  </div>

</template>

<script>
import MainFooter from "../partials/MainFooter";
import MainHeader from "../partials/MainHeader";
import SideMenu from "../partials/SideMenu";

export default {
  components: {
    MainFooter,
    MainHeader,
    SideMenu
  },
  mounted: function() {
    // initialize Metronic components
    window.KTUtil.init();
    window.KTLayout.initHeader();
    window.KTLayout.initAside();
    window.KTApp.init();

  }
};
</script>
