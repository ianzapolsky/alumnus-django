define([
  'jquery',
  'underscore',
  'backbone',
], function($, _, Backbone) {
  
  var UserLoginView = Backbone.View.extend({
    
    el: '.form-container',
  
    initialize: function() {
      console.log('UserLoginView initialize');
    },

    events: { 
      'change #username': 'validateUsername',
      'change #password': 'validatePassword'
    },

    validateUsername: function() {
      var data = {'username': $('#username').val()};
      $.ajax({
        url: '/api/users/exists/',
        type: 'POST',
        data: data,
        success: function(data) {
          if (data.exists) {
            document.getElementById('username').setCustomValidity('');
          } else {
            document.getElementById('username').setCustomValidity('Username does not exist.');
          }
        }
      });
    },

    validatePassword: function() {
      var data = {'username': $('#username').val(), 'password': $('#password').val()};
      $.ajax({
        url: '/api/users/check-password/',
        type: 'POST',
        data: data,
        success: function(data) {
          if (data.valid) {
            document.getElementById('password').setCustomValidity('');
          } else {
            document.getElementById('password').setCustomValidity('Password is not valid.');
          }
        }
      });

    }

  });

  return UserLoginView;

});

    
