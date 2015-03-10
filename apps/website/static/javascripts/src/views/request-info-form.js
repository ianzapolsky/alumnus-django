define([
  'jquery',
  'underscore',
  'backbone',
], function($, _, Backbone) {

  var RequestInfoFormView = Backbone.View.extend({

    el: '.member-list-container',

    messages: [],

    messagesSent: 0,

    initialize: function() {
      console.log('RequestInfoFormView initialize');
    },

    events: { 
      'click #send-info-request': 'handleSendAsync'
    },

    formIsValid: function () {
      var valid = true
      // Check for at least one checked Member
      if ($('input[type=checkbox]:checked').length === 0) {
        this.signalError('Please check at least one Member.');
        valid = false
      } 
      if (this.checkRequired() && valid) {
        this.signalSuccess();
        return true;
      } else {
        this.renderErrors();
        return false;
      }
    },

    handleSendAsync: function (ev) {
      ev.preventDefault();
      this.messagesSent = 0;
      var _this = this;
      if (this.formIsValid()) {
        _.forEach($('input[type=checkbox]:checked'), function(el) {
          var loader = '<div id="loader"><img src="/static/images/ajax-loader.gif"></div>'; 
          $(loader).appendTo($(el).parent().parent());
          _this.sendRequestToMember(el);
        });
      }
    },

    sendRequestToMember: function (el) {
      var _this = this;
      var data = {
        member_id: $(el).attr('data-member-id'),
        subject: $('#subject').val(),
        message: $('#message').val(),
        from: $('#from').val()
      };
      $.ajax({
        url: '/api/members/request-update/',
        type: 'POST',
        data: data,
        success: function (data) {
          if (data.error) {
            $(el).parent().parent().find('#loader').remove();
            var content = _.template($('#errors-template').html(), {Errors: [data.message]});
            $('#messages-container').html(content);
          } else {
            $(el).parent().parent().find('#loader').remove();
            $(el).parent().parent().css('background-color', 'rgba(0,255,0,0.25)');
            $(el).prop('checked', false);

            _this.messagesSent += 1;
            if (_this.messagesSent === 1) var msg = '1 request successfully sent.';
            else var msg = _this.messagesSent + ' requests sent successfully.';
            var content = _.template($('#messages-template').html(), {Messages: [msg]});
            $('#messages-container').html(content);
          }
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
          _this.signalRequiredError(field);
        }
      });
      return valid;
    },

    signalRequiredError: function(field) {
      this.messages.push(field.siblings('label').text() + ' This field is required.');
    },

    signalError: function(errorMsg) {
      this.messages.push(errorMsg);
    },

    signalSuccess: function() {
      $('#messages-container').html('');
      window.scroll(0,0);
    },

    renderErrors: function() {
      var content = _.template($('#errors-template').html(), {Errors: this.messages});
      $('#messages-container').html(content);
      this.messages = [];
      window.scroll(0,0);
    }

  });
  
  return RequestInfoFormView;

});
  
