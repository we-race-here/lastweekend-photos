const PUBLIC_PATH = "/static/vue/";

module.exports = {
  publicPath: PUBLIC_PATH,
  productionSourceMap: false,
  runtimeCompiler: true,
  chainWebpack: config => {
    config.externals({
      jquery: "jQuery",
      moment: "moment"
    });
  },
  devServer: {
    setup: function(app) {
      app.get("/", function(req, res) {
        res.redirect(PUBLIC_PATH);
      });
    },
    watchOptions: {
      poll: true
    },
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true
      }
    }
  }
};
