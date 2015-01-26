define([
  'jquery',
  'underscore',
  'backbone',
], function($, _, Backbone) {
  
  var TableButtonsView = Backbone.View.extend({
    
    el: '.member-list-container',
  
    initialize: function() {
      console.log('TableButtonsView initialize');
    },

    events: { 
      'click #check-all': 'checkAll',
      'click #uncheck-all': 'uncheckAll',
    },

    checkAll: function( ev ) {
      ev.preventDefault();
      $('input[type=checkbox]').prop('checked', true);
    },

    uncheckAll: function( ev ) {
      ev.preventDefault();
      $('input[type=checkbox]').prop('checked', false);
    }

  });

  return TableButtonsView;

});

    
