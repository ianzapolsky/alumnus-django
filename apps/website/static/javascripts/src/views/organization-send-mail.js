define([
  'jquery',
  'underscore',
  'backbone',
  'src/views/form-validation',
], function($, _, Backbone) {
  
  var OrganizationSendMailView = Backbone.View.extend({
    
    el: '.member-list-container',

    messagesSent: 0,
  
    initialize: function() {
      console.log('OrganizationSendMailView initialize');
    },

    events: { 
      'change #subject': 'validateRequired',
      'change #message': 'validateRequired',
      'keydown #subject': 'removeRequiredError',
      'keydown #message': 'removeRequiredError',

      'click #send-mail': 'handleSendAsync',
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

    handleSendAsync: function (ev) {
      ev.preventDefault();
      var _this = this;
      if (this.formIsValid()) {
        _.forEach($('input[type=checkbox]:checked'), function(el) {
          var loader = '<div id="loader"><img src="/static/images/ajax-loader.gif"></div>'; 
          $(loader).appendTo($(el).parent().parent());
          _this.sendMailToMember(el);
        });
      }
    },

    sendMailToMember: function (el) {
      var _this = this;
      var address = $(el).attr('data-member-email');
      var recipients = [address];
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
        success: function (data) {
          $(el).parent().parent().find('#loader').remove();
          $(el).parent().parent().css('background-color', 'rgba(0,255,0,0.25)');
          $(el).prop('checked', false);
          _this.messagesSent += 1;

          if (_this.messagesSent === 1)
            var msg = '1 email successfully sent.';
          else
            var msg = _this.messagesSent + ' emails sent successfully.';
          var messages = [msg];
          var content = _.template($('#messages-template').html(), {Messages: messages});
          $('#messages-container').html(content);
        }
      });
    },

    checkRequired: function () {
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

    
