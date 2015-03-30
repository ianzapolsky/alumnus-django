require.config({
  shim: {
    'common': {'deps': ['jquery']}
  },
  paths: {
    'common': 'dist/lib/common',
    'backbone': 'dist/lib/backbone',
    'jquery': 'dist/lib/jquery',
    'underscore': 'dist/lib/underscore',
  }
});

require([
  'common'
], function() {
  console.log('loaded frontend scripts');
});

require([
  'jquery',
  'dist/src/util/util',
], function($, util) {
  $.ajaxSetup({
    headers: { 'X-CSRFToken': util.getCookie('csrftoken') }
  });
});

