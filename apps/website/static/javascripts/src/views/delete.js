define([
  'jquery',
  'underscore',
  'backbone',
], function($, _, Backbone) {
  
  var DeleteView = Backbone.View.extend({
    
    el: '.form-container',
  
    initialize: function() {
      console.log('DeleteView initialize');
    },

    events: { 
      'click .btn-delete': 'handleDelete'
    },

    handleDelete: function( ev ) {
      event.preventDefault();
      var data = {member_id: $('#member_id').val()}
      $.ajax({
        url: '/api/members/delete/',
        type: 'POST',
        dataType: 'json',
        data: data,
        headers: { 'X-CSRFToken': this.getCookie('csrftoken') },
        success: function(msg) {
          alert(msg);
        }
      });
    },

    getCookie: function( c_name ) {
      if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1) {
          c_start = c_start + c_name.length + 1;
          c_end = document.cookie.indexOf(";", c_start);
          if (c_end == -1) c_end = document.cookie.length;
          return unescape(document.cookie.substring(c_start,c_end));
        }
      }
      return "";
    }

  });

  return DeleteView;

});

    
