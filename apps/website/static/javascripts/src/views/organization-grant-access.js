define([
  'jquery',
  'underscore',
  'backbone',
], function($, _, Backbone) {

  var OrganizationGrantAccessView = Backbone.View.extend({

    el: '#grant-access-container',

    initialize: function() {
      console.log('OrganizationGrantAccessView initialize');
    },

    events: { 
      'click #btn-submit': 'handleAccessGrant',
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

    handleAccessGrant: function (ev) {
      ev.preventDefault();
      var _this = this;
      if (this.formIsValid()) {
        var data = {
          organization_id: $('#organization-id').val(),
          username: $('#username').val()
        };
        $.ajax({
          url: '/api/organizations/grant-access/',
          type: 'POST',
          data: data,
          success: function (data) {
            if (data.error) {
              var content = _.template($('#errors-template').html(), {Errors: [data.message]});
              $('#messages-container').html(content);
            } else {
              var content = _.template($('#messages-template').html(), {Messages: [data.message]});
              $('#messages-container').html(content);
            }
          }
        });
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
    }

  });
  
  return OrganizationGrantAccessView;

});
  
