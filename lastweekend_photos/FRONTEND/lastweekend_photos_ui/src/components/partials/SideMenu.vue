<template>
  <div class="kt-aside  kt-aside--fixed  kt-grid__item kt-grid kt-grid--desktop kt-grid--hor-desktop" id="kt_aside">
    <!-- begin:: Aside Menu -->
    <div class="kt-aside-menu-wrapper kt-grid__item kt-grid__item--fluid" id="kt_aside_menu_wrapper">
      <div id="kt_aside_menu" class="kt-aside-menu " data-ktmenu-vertical="1" data-ktmenu-scroll="1"
           data-ktmenu-dropdown-timeout="500">
        <ul class="kt-menu__nav ">
          <li class="kt-menu__item" :class="{'kt-menu__item--active': isActive($rns.DASHBOARD)}" aria-haspopup="true">
            <a is="router-link" :to="{name: $rns.DASHBOARD}" class="kt-menu__link ">
              <i class="kt-menu__link-icon flaticon2-protection"></i><span class="kt-menu__link-text">Dashboard</span>
            </a>
          </li>
          <li class="kt-menu__item" :class="{'kt-menu__item--active': isActive($rns.MY_PHOTOS)}" aria-haspopup="true">
            <a is="router-link" :to="{name: $rns.MY_PHOTOS}" class="kt-menu__link ">
              <i class="kt-menu__link-icon flaticon-photo-camera"></i><span class="kt-menu__link-text">My Photos</span>
            </a>
          </li>
          <li class="kt-menu__item " aria-haspopup="true"><a href="#" class="kt-menu__link "><i
                  class="kt-menu__link-icon flaticon2-calendar-6"></i><span class="kt-menu__link-text">Events</span></a>
          </li>
          <li class="kt-menu__item " aria-haspopup="true"><a href="#" class="kt-menu__link "><i
                  class="kt-menu__link-icon flaticon2-calendar-4"></i><span
                  class="kt-menu__link-text">Calendar</span></a></li>
          <li class="kt-menu__item " aria-haspopup="true"><a href="#" class="kt-menu__link "><i
                  class="kt-menu__link-icon flaticon2-gear"></i><span class="kt-menu__link-text">Settings</span></a>
          </li>
        </ul>
      </div>
    </div>
    <!-- end:: Aside Menu -->
  </div>

</template>

<script>
  import UtilMixin from "../mixins/UtilMixin";

  export default {
    data: function () {
      return {};
    },
    mixins: [UtilMixin],
    methods: {
      isActive: function () {
        return Array.from(arguments).indexOf(this.$route.name) >= 0;
      }
    },
    mounted: function () {
    }
  };
</script>