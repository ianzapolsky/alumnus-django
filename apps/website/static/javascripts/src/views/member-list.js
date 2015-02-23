define([
  'jquery',
  'underscore',
  'backbone',
], function($, _, Backbone) {
  
  var MemberListView = Backbone.View.extend({
    
    el: '#member-list-container',
  
    initialize: function() {
      console.log('MemberListView initialize');
    },

    events: { 
      'click #member-send-mail': 'renderSendMailForm',
      'click #send-mail': 'handleSend',
    },

    formIsValid: function () {
      var valid = true
      // Check for at least one checked Member
      if ($('input:checked').length === 0) {
        this.signalError('Please check at least one Member.');
        valid = false
      } else {
        this.signalSuccess();
      }
      return valid; 
    },

    signalError: function(errorMsg) {
      var errors = [errorMsg];
      var content = _.template( $('#errors-template').html(), {Errors: errors});
      $('#member-list-errors').html(content);
      $('#send-mail-container').html('');
    },

    signalSuccess: function() {
      $('#member-list-errors').html('');
    },

    renderSendMailForm: function () {
      if (this.formIsValid()) {
        var content = _.template( $('#send-mail-template').html());
        $('#send-mail-container').html(content);
      }
    },

    showLoading: function() {
      // add the overlay with loading image to the page
       var over = '<div class="overlay">' +
            '<img class="loading" src="/static/images/ajax-loader.gif">' +
            '</div>'; 
      $(over).appendTo('body');
      window.scrollTo(0,0);
    },

    hideLoading: function() {
      $('.overlay').remove();
    },

    handleSend: function (ev) {
      ev.preventDefault();
      if (this.formIsValid()) {
        this.showLoading();
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
    },

  });

  return MemberListView;

});

    
