define([
  'jquery',
  'underscore',
  'backbone',
], function($, _, Backbone) {
  
  var MemberListSendMailView = Backbone.View.extend({
    
    el: '#form-container',
  
    initialize: function() {
      console.log('MemberListSendMailView initialize');
    },

    events: { 
      'change #subject': 'validateRequired',
      'change #message': 'validateRequired',

      'keydown #subject': 'removeRequiredError',
      'keydown #message': 'removeRequiredError',

      'click #send-mail': 'handleSend'
    },

    formIsValid: function () {
      if (this.checkRequired())
        return true;
      return false;
    },

    handleSend: function( ev ) {
      ev.preventDefault();
      if (this.formIsValid()) {
        this.showLoading(); 
        var _this = this;
        var data = {
          memberlist_id: $('#memberlist-id').val(),
          message: $('#message').val(),
          subject: $('#subject').val()
        };
        $.ajax({
          url: '/api/memberlists/send-mail/',
          type: 'POST',
          data: data,
          success: function(data) {
            _this.hideLoading();
            if (data.redirect) {
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

  return MemberListSendMailView;

});

    
