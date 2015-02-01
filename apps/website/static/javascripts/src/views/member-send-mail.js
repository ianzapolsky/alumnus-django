define([
  'jquery',
  'underscore',
  'backbone',
], function($, _, Backbone) {
  
  var MemberSendMailView = Backbone.View.extend({
    
    el: '#form-container',
  
    initialize: function() {
      console.log('MemberSendMailView initialize');
    },

    events: { 
      'click #send-mail': 'handleSend'
    },

    handleSend: function( ev ) {
      ev.preventDefault();
      var data = {
        member_id: $('#member-id').val(),
        message: $('#message').val(),
        subject: $('#subject').val()
      };
      $.ajax({
        url: '/api/members/send-mail/',
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

  return MemberSendMailView;

});

    
