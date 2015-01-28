define([
  'jquery',
  'underscore',
  'backbone',
], function($, _, Backbone) {
  
  var UserRegisterView = Backbone.View.extend({
    
    el: '#register-container',

    initialize: function() {
      console.log('UserRegisterView initialize');
    },

    events: { 
      'change #username': 'validateUsername',
      'change #email': 'validateEmail',
      'change #password2': 'validatePasswords',

      'keydown #username': 'removeRequiredError',
      'keydown #email': 'removeRequiredError',
      'keydown #password1': 'removeRequiredError',
      'keydown #password2': 'removeRequiredError',

      'click #btn-submit': 'checkRequired'
    },

    validateUsername: function() {
      var _this = this;
      var data = {'username': $('#username').val()};
      $.ajax({
        url: '/api/users/exists/',
        type: 'POST',
        data: data,
        success: function(data) {
          $username = $('#username');
          if (data.exists) {
            _this.signalError($username, 'Username is already taken.');
          } else {
            _this.signalSuccess($username);
          }
        }
      });
    },

    validateEmail: function() {
      var $email = $('#email');
      var x = $email.val();
      var atpos = x.indexOf("@");
      var dotpos = x.lastIndexOf(".");
      if (atpos< 1 || dotpos<atpos+2 || dotpos+2>=x.length) {
        this.signalError($email, 'Not a valid e-mail address.');
      } else {
        this.signalSuccess($email);
      }
    },

    validatePasswords: function() {
      password1 = $('#password1').val();
      password2 = $('#password2').val();
      if (password1 != password2) {
        this.signalError($('#password2'), 'Passwords must match.');
        this.signalError($('#password1'), '');
      } else {
        this.signalSuccess($('#password1'));
        this.signalSuccess($('#password2'));
      }
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

  return UserRegisterView;

});

    
