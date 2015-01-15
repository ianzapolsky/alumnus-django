define([
  'jquery',
  'underscore',
  'backbone',
], function($, _, Backbone) {
  
  var MemberDetailView = Backbone.View.extend({
    
    el: '.form-container',
  
    initialize: function() {
      console.log('MemberDetailView initialize');
    },

    events: { 
      'click #member-update-request': 'handleUpdateRequest',
      'click #member-delete': 'handleDelete'
    },

    handleUpdateRequest: function( ev ) {
      ev.preventDefault();
      var data = {member_id: $('#member-id').val()};
      $.ajax({
        url: '/api/members/request-update/',
        type: 'POST',
        data: data,
        success: function(msg) {
          console.log(msg);
        }
      });
    },

    handleDelete: function( ev ) {
      ev.preventDefault();
      var data = {member_id: $('#member-id').val()};
      $.ajax({
        url: '/api/members/delete/',
        type: 'POST',
        data: data,
        success: function(data) {
          window.location.replace(data.redirect);
          // $('#member-title').text('Member has been deleted.');
        }
      });
    }

  });

  return MemberDetailView;

});

    
