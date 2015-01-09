define([
  'jquery',
  'underscore',
  'backbone',
], function($, _, Backbone) {
  
  var BaseView = Backbone.View.extend({

    el: '.base',

    initialize: function() {
      console.log('hello world');
    }

  });
  
  return BaseView;
});

    
