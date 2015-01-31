require.config({
  shim: {
    "bootstrap": {"deps": ['jquery']},
    "jquery-easing": {"deps": ['jquery']},
    "scrolling-nav": {"deps": ['jquery']},
  },
  paths: {
    "backbone": "lib/backbone-amd/backbone",
    "bootstrap": "lib/scrolling-nav-1.0.1/js/bootstrap.min",
    "jquery": "lib/jquery/dist/jquery",
    "jquery-easing": "lib/scrolling-nav-1.0.1/js/jquery.easing.min",
    "scrolling-nav": "lib/scrolling-nav-1.0.1/js/scrolling-nav",
    "underscore": "lib/underscore-amd/underscore"
  }
});

require([
  'jquery',
  'bootstrap',
  'jquery-easing',
  'scrolling-nav',
], function() {
  console.log('loaded frontend scripts');
});

require([
  'jquery',
  'src/util/util',
], function($, util) {
  $.ajaxSetup({
    headers: { 'X-CSRFToken': util.getCookie('csrftoken') }
  });
});
