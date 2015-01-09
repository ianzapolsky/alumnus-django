require.config({
  paths: {
    "jquery": "lib/jquery/dist/jquery",
    "underscore": "lib/underscore-amd/underscore",
    "backbone": "lib/backbone-amd/backbone"
  }
});

require(['src/views/base'], function(BaseView) {
  new BaseView();
});

