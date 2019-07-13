export default {
  data: function() {
    return {
      loadingOverlay: false
    };
  },
  watch: {
    loadingOverlay: function(value) {
      if (value) {
        window.KTApp.block(this.$el, {
          overlayColor: "#000000",
          type: "loader",
          state: "primary",
          message: "Loading..."
        });
      } else {
        window.KTApp.unblock(this.$el);
      }
    }
  }
};
