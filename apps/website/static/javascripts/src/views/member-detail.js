define([
  'jquery',
  'underscore',
  'backbone',
], function($, _, Backbone) {
  
  var MemberDetailView = Backbone.View.extend({
    
    el: '.member-detail-container',

    messages: [],
  
    initialize: function() {
      console.log('MemberDetailView initialize');
    },

    events: { 
      'click #send-mail': 'handleSendAsync',
      'click #send-info-request': 'handleUpdateRequest',
      'click #member-send-mail': 'renderSendMailForm',
      'click #member-request-info': 'renderRequestInfoForm',
      'click #member-delete': 'handleDelete'
    },

    formIsValid: function () {
      if (this.checkRequired()) {
        this.signalSuccess();
        return true;
      } else {
        this.renderErrors();
        return false;
      }
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
    },

    renderSendMailForm: function () {
      var content = _.template( $('#send-mail-template').html());
      $('#send-mail-container').html(content);
    },

    renderRequestInfoForm: function() {
      var content = _.template( $('#send-info-request-template').html());
      $('#send-mail-container').html(content);
    },

    handleUpdateRequest: function (ev) {
      ev.preventDefault();
      this.messagesSent = 0;
      var _this = this;
      if (this.formIsValid()) {
        _this.sendRequestToMember();
      }
    },

    sendRequestToMember: function (el) {
      this.showLoading();
      var _this = this;
      var data = {
        member_id: $('#member-id').val(),
        subject: $('#subject').val(),
        message: $('#message').val()
      };
      $.ajax({
        url: '/api/members/request-update/',
        type: 'POST',
        data: data,
        success: function (data) {
          _this.hideLoading();
          _this.messagesSent += 1;
          if (_this.messagesSent === 1) var msg = '1 request successfully sent.';
          else var msg = _this.messagesSent + ' requests sent successfully.';
          var content = _.template($('#messages-template').html(), {Messages: [msg]});
          $('#messages-container').html(content);
        }
      });
    },

    handleSendAsync: function (ev) {
      ev.preventDefault();
      this.messagesSent = 0;
      var _this = this;
      if (this.formIsValid()) {
        _this.sendMailToMember();
      }
    },

    sendMailToMember: function (el) {
      this.showLoading();
      var _this = this;
      var data = {
        member_id: $('#member-id').val(),
        message: $('#message').val(),
        subject: $('#subject').val()
      };
      $.ajax({
        url: '/api/members/send-mail/',
        type: 'POST',
        data: data,
        success: function (data) {
          _this.hideLoading();
          _this.messagesSent += 1;
          if (_this.messagesSent === 1) var msg = '1 email successfully sent.';
          else var msg = _this.messagesSent + ' emails sent successfully.';
          var content = _.template($('#messages-template').html(), {Messages: [msg]});
          $('#messages-container').html(content);
        }
      });
    },

    handleDelete: function( ev ) {
      ev.preventDefault();
      var check = confirm("Are you sure you want to delete this Member?");
      if (check == true) {
        this.showLoading();
        var _this = this;
        var data = {member_id: $('#member-id').val()};
        $.ajax({
          url: '/api/members/delete/',
          type: 'POST',
          data: data,
          success: function(data) {
            _this.hideLoading();
            if (data.error) {
              var content = _.template($('#errors-template').html(), {Errors: [data.message]});
              $('#messages-container').html(content);
            } else if (data.redirect) {
              window.location.replace(data.redirect);
            }
          }
        });
      }
    },

    showLoading: function() {
      // add the overlay with loading image to the page
       var over = '<div class="overlay">' +
            '<img class="loading" src="/static/images/ajax-loader.gif">' +
            '</div>'; 
      $(over).appendTo('body');
    },

    hideLoading: function() {
      $('.overlay').remove();
    },

  });

  return MemberDetailView;

});

    
