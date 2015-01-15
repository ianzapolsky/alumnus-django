define([
  'jquery',
  'underscore',
  'backbone',
], function($, _, Backbone) {
  
  var MemberListSendMailView = Backbone.View.extend({
    
    el: '.form-container',
  
    initialize: function() {
      console.log('MemberListSendMailView initialize');
    },

    events: { 
      'click #send-mail': 'handleSend'
    },

    handleSend: function( ev ) {
      ev.preventDefault();
      var data = {
        memberlist_id: $('#memberlist-id').val(),
        message: $('#message').val(),
        subject: $('#subject').val()
      };
      $.ajax({
        url: '/api/memberlists/send-mail/',
        type: 'POST',
        data: data,
        success: function(msg) {
          console.log(msg)
        }
      });
    }

  });

  return MemberListSendMailView;

});

    
