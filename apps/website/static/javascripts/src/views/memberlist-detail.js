define([
  'jquery',
  'underscore',
  'backbone',
], function($, _, Backbone) {
  
  var MemberListDetailView = Backbone.View.extend({
    
    el: '.centered',
  
    initialize: function() {
      console.log('MemberListDetailView initialize');
    },

    events: { 
      'click #memberlist-delete': 'handleDelete'
    },

    handleDelete: function( ev ) {
      ev.preventDefault();
      var data = {memberlist_id: $('#memberlist-id').val()};
      $.ajax({
        url: '/api/memberlists/delete/',
        type: 'POST',
        data: data,
        success: function(data) {
          if (data.redirect) {
            window.location.replace(data.redirect);
          }
        }
      });
    }

  });

  return MemberListDetailView;

});

    
