define([
  'jquery',
  'underscore',
  'backbone',
], function($, _, Backbone) {
  
  var UserLoginView = Backbone.View.extend({
    
    el: '#login-container',
  
    initialize: function() {
      console.log('UserLoginView initialize');
    },

    events: { 
      'keydown #username': 'removeRequiredError',
      'keydown #password': 'removeRequiredError',
      'click #btn-submit': 'checkRequired',
    },

    removeRequiredError: function (ev) {
      if ($(ev.currentTarget).val() != '') {
        $(ev.currentTarget).parent().removeClass('has-error');
        $(ev.currentTarget).tooltip('destroy');
      }
    },

    checkRequired: function (ev) {
      ev.preventDefault();
      var _this = this;
      var valid = true;
      _.forEach($('input,textarea,select').filter('[required]:visible'), function(field) {
        var field = $(field);
        if (field.val() === '') {
          valid = false;
          _this.signalError(field, 'This field is required.');
        }
      });
      if (valid) {
        $('form').submit();
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

  return UserLoginView;

});

    
