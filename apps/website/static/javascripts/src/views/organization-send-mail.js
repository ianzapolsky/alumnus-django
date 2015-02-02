define([
  'jquery',
  'underscore',
  'backbone',
], function($, _, Backbone) {
  
  var OrganizationSendMailView = Backbone.View.extend({
    
    el: '.member-list-container',
  
    initialize: function() {
      console.log('OrganizationSendMailView initialize');
    },

    events: { 
      'change #subject': 'validateRequired',
      'change #message': 'validateRequired',

      'keydown #subject': 'removeRequiredError',
      'keydown #message': 'removeRequiredError',

      'click #send-mail': 'handleSend',
    },

    formIsValid: function () {
      var valid = true
      // Check for at least one checked Member
      if ($('input:checked').length === 0) {
        this.signalError($('#member-list-members'), 'Please check at least one Member.');
        valid = false
      } else {
        this.signalSuccess($('#member-list-members'));
      }
      
      if (this.checkRequired() && valid === true)
        return true;
      return false;
    },

    handleSend: function (ev) {
      ev.preventDefault();
      if (this.formIsValid()) {
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

    checkRequired: function () {
      console.log('hi');
      var _this = this;
      var valid = true;
      _.forEach($('input,textarea,select').filter('[required]:visible'), function(field) {
        var field = $(field);
        if (field.val() === '') {
          valid = false;
          _this.signalError(field, 'This field is required.');
        }
      });
      return valid;
    },

    removeRequiredError: function (ev) {
      if ($(ev.currentTarget).val() != '') {
        $(ev.currentTarget).parent().removeClass('has-error');
        $(ev.currentTarget).tooltip('destroy');
      }
    },
  
    validateRequired: function (ev) {
      if ($(ev.currentTarget).val() === '') {
        this.signalError($(ev.currentTarget), 'This field is required.');
      }
    },

    signalError: function($container, errorMsg) {
      $container.parent().removeClass('has-success');
      $container.parent().addClass('has-error');
      $container.tooltip({'trigger': 'manual', 'placement': 'bottom', 'title': errorMsg}).tooltip('show');
    },

    signalSuccess: function($container) {
      $container.parent().removeClass('has-error');
      $container.parent().addClass('has-success');
      $container.tooltip('destroy');
    },

  });

  return OrganizationSendMailView;

});

    
