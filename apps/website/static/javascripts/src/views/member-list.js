define([
  'jquery',
  'underscore',
  'backbone',
], function($, _, Backbone) {
  
  var MemberListView = Backbone.View.extend({
    
    el: '.centered',
  
    initialize: function() {
      console.log('MemberListView initialize');
    },

    events: { 
      'click tr': 'followLink'
    },

    followLink: function( ev ) {
      ev.preventDefault();
      if ($(ev.currentTarget).attr('href')) {
        window.location.href = $(ev.currentTarget).attr('href');
      } 
    },

  });

  return MemberListView;

});

    
