define([
  'jquery',
  'underscore',
  'backbone',
], function($, _, Backbone) {
  
  var UserRegisterView = Backbone.View.extend({
    
    el: '.form-container',
  
    initialize: function() {
      console.log('UserRegisterView initialize');
    },

    events: { 
      'change #username': 'validateUsername',
      'change #password2': 'validatePasswords'
    },

    validateUsername: function() {
      var data = {'username': $('#username').val()};
      $.ajax({
        url: '/api/users/exists/',
        type: 'POST',
        data: data,
        success: function(data) {
          if (data.exists) {
            document.getElementById('username').setCustomValidity('Username is already taken.');
          } else {
            document.getElementById('username').setCustomValidity('');
          }
        }
      });
    },

    validatePasswords: function() {
      password1 = $('#password1').val();
      password2 = $('#password2').val();
      if (password1 != password2) {
        document.getElementById('password1').setCustomValidity('Passwords must match.');
      } else {
        document.getElementById('password1').setCustomValidity('');
      }
    }

  });

  return UserRegisterView;

});

    
