<style scoped>
.kt-user-card__email {
  color: #9e9d9d;
}
.kt-header__topbar .kt-header__topbar-item.kt-header__topbar-item--user .kt-header__topbar-wrapper img {
  width: 34px;
  height: 34px;
}
</style>
<template>
  <div id="kt_header" class="kt-header kt-grid kt-grid--ver  kt-header--fixed ">

    <div class="kt-header__brand kt-grid__item  " id="kt_header_brand">
      <div class="kt-header__brand-logo">
        <a href="/">
          <img alt="Logo" :src="`${$publicPath}resources/images/logo-6.png`" />
        </a>
      </div>
    </div>

    <h3 class="kt-header__title kt-grid__item">
      Lastweekend Photos
    </h3>

    <button class="kt-header-menu-wrapper-close" id="kt_header_menu_mobile_close_btn"><i class="la la-close"></i></button>
    <div class="kt-header-menu-wrapper kt-grid__item kt-grid__item--fluid" id="kt_header_menu_wrapper">
      <div id="kt_header_menu" class="kt-header-menu kt-header-menu-mobile  kt-header-menu--layout-default ">
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
          <!--<li class="kt-menu__item  kt-menu__item--active " aria-haspopup="true"><a href="#" class="kt-menu__link "><span class="kt-menu__link-text">Dashboard</span></a></li>-->
        </ul>
      </div>
    </div>

    <div class="kt-header__topbar">
      <div class="kt-header__topbar-item kt-header__topbar-item--search dropdown" id="kt_quick_search_toggle">
        <div class="kt-header__topbar-wrapper" data-toggle="dropdown" data-offset="10px,0px">
          <span class="kt-header__topbar-icon"><i class="flaticon2-search-1"></i></span>
        </div>
        <div class="dropdown-menu dropdown-menu-fit dropdown-menu-right dropdown-menu-anim dropdown-menu-lg">
          <div class="kt-quick-search kt-quick-search--inline" id="kt_quick_search_inline">
            <form method="get" class="kt-quick-search__form">
              <div class="input-group">
                <div class="input-group-prepend"><span class="input-group-text"><i
                        class="flaticon2-search-1"></i></span></div>
                <input type="text" class="form-control kt-quick-search__input" placeholder="Search...">
                <div class="input-group-append"><span class="input-group-text"><i
                        class="la la-close kt-quick-search__close"></i></span></div>
              </div>
            </form>
            <div class="kt-quick-search__wrapper kt-scroll" data-scroll="true" data-height="300"
                 data-mobile-height="200">
            </div>
          </div>
        </div>
      </div>

      <div class="kt-header__topbar-item dropdown">
        <div class="kt-header__topbar-wrapper" data-toggle="dropdown" data-offset="10px,0px">
          <span class="kt-header__topbar-icon kt-header__topbar-icon--success"><i
                  class="flaticon2-bell-alarm-symbol"></i></span>
          <span class="kt-hidden kt-badge kt-badge--danger"></span>
        </div>
      </div>

      <div class="kt-header__topbar-item dropdown">
        <div class="kt-header__topbar-wrapper" data-toggle="dropdown" data-offset="10px,0px">
          <span class="kt-header__topbar-icon kt-header__topbar-icon--warning"><i class="flaticon2-gear"></i></span>
        </div>
      </div>

      <div class="kt-header__topbar-item kt-header__topbar-item--user">
        <div class="kt-header__topbar-wrapper" data-toggle="dropdown" data-offset="10px,0px">
          <img v-if="$store.state.currentUser.avatar" alt="Pic" :src="$store.state.currentUser.avatar"/>
          <span v-else class="kt-header__topbar-icon">{{ $store.getters.userDisplayName.slice(0, 1) }}</span>
        </div>
        <div class="dropdown-menu dropdown-menu-fit dropdown-menu-right dropdown-menu-anim dropdown-menu-xl">

          <div class="kt-user-card kt-user-card--skin-dark kt-notification-item-padding-x"
               :style="`background-image: url(${$publicPath}resources/images/bg-1.jpg)`">
            <div class="kt-user-card__avatar">
              <img v-if="$store.state.currentUser.avatar" alt="Pic" :src="$store.state.currentUser.avatar"/>
              <span v-else class="kt-badge kt-badge--lg kt-badge--rounded kt-badge--bold kt-font-success">{{ $store.getters.userDisplayName.slice(0, 1) }}</span>
            </div>
            <div class="kt-user-card__name">
              {{ $store.getters.userDisplayName }}
              <p class="small kt-user-card__email">{{ $store.state.currentUser.email }}</p>
            </div>
          </div>

          <div class="kt-notification">
            <a is="router-link" :to="{name: $rns.MY_PROFILE}" class="kt-notification__item">
              <div class="kt-notification__item-icon">
                <i class="flaticon2-calendar-3 kt-font-success"></i>
              </div>
              <div class="kt-notification__item-details">
                <div class="kt-notification__item-title kt-font-bold">
                  My Profile
                </div>
                <div class="kt-notification__item-time">
                  User, Racer and Staff promotors profile
                </div>
              </div>
            </a>
            <a href="javascript:" class="kt-notification__item">
              <div class="kt-notification__item-icon">
                <i class="flaticon2-settings kt-font-danger"></i>
              </div>
              <div class="kt-notification__item-details">
                <div class="kt-notification__item-title kt-font-bold">
                  Settings
                </div>
                <div class="kt-notification__item-time">
                  User setttings and configuration
                </div>
              </div>
            </a>
            <a href="javascript:" class="kt-notification__item">
              <div class="kt-notification__item-icon">
                <i class="flaticon-questions-circular-button kt-font-info"></i>
              </div>
              <div class="kt-notification__item-details">
                <div class="kt-notification__item-title kt-font-bold">
                  FAQ
                </div>
                <div class="kt-notification__item-time">
                  Frequently Asked Questions
                </div>
              </div>
            </a>
            <div class="kt-notification__custom">
              <a href="javascript:" @click="logout" class="btn btn-label-danger btn-sm btn-bold">
                <i class="flaticon-logout"></i>
                Sign Out
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
  import UtilMixin from "../mixins/UtilMixin";

  export default {
    mixins: [UtilMixin],
    components: {},
    methods: {
      logout: function () {
        var self = this;
        this.showInfo("Logging out ...");
        this.$http.delete("session").then(
            function () {
              self.$store.state.currentUser = {};
            },
            function (error) {
              self.showDefaultServerError(error);
            }
        );
      },
      isActive: function () {
        return Array.from(arguments).indexOf(this.$route.name) >= 0;
      }
    },
    computed: {},
    mounted: function () {
    }
  };
</script>