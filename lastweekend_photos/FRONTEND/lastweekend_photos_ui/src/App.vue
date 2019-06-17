<style scoped>
.app-version-tag {
  right: unset;
  left: 80px;
  border-radius: 0;
  background-color: #b37b11;
}
</style>

<template>
  <div class="kt-grid kt-grid--hor kt-grid--root">
    <span title="Ui Version" class="fixed-top badge badge-danger app-version-tag">{{ $appVersion }}</span>
    <template v-if="$store.getters.isLoadedUser">
      <main-layout></main-layout>
    </template>
    <template v-else>
      <login-page></login-page>
    </template>
    <version-alert v-if="mismatchVersion" :new-version="newAppVersion"></version-alert>
  </div>

</template>

<script>
import LoginPage from "./components/pages/LoginPage";
import VersionAlert from "./components/partials/VersionAlert";
import MainLayout from "./components/layouts/MainLayout";
import UtilMixin from "./components/mixins/UtilMixin"

export default {
  name: "App",
  components: { MainLayout, VersionAlert, LoginPage },
  mixins: [UtilMixin],
  data() {
    return {
      mismatchVersion: false,
      newAppVersion: null
    };
  },
  methods: {
    onSessionExpired: function() {
      this.$store.state.currentUser = {};
    },
    onMismatchVersion: function(newVersion) {
      this.mismatchVersion = true;
      this.newAppVersion = newVersion;
    }
  },
  mounted: function() {
    this.$eventsBus.$on("user:session-expired", this.onSessionExpired);
    this.$eventsBus.$on("ui:mismatch-version", this.onMismatchVersion);
  },
  destroyed: function() {
    this.$eventsBus.$off("user:session-expired", this.onSessionExpired);
    this.$eventsBus.$off("ui:mismatch-version", this.onMismatchVersion);
  }
};
</script>
