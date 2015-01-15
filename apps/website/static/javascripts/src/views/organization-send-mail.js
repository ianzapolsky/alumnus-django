define([
  'jquery',
  'underscore',
  'backbone',
], function($, _, Backbone) {
  
  var OrganizationSendMailView = Backbone.View.extend({
    
    el: '.send-mail-container',
  
    initialize: function() {
      console.log('OrganizationSendMailView initialize');
    },

    events: { 
      'click #send-mail': 'handleSend'
    },

    handleSend: function( ev ) {
      ev.preventDefault();
      recipients = []
      _.forEach($('input[type=checkbox]:checked'), function(el) {
        recipients.push($(el).attr('data-member-email'));
      });
      var data = {
        organization_id: $('#organization-id').val(),
        recipients: JSON.stringify(recipients),
        message: $('#message').val(),
        subject: $('#subject').val()
      };
      $.ajax({
        url: '/api/organizations/send-mail/',
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

  return OrganizationSendMailView;

});

    
