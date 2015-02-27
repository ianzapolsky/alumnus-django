define([
  'jquery',
  'underscore',
  'backbone',
], function($, _, Backbone) {
  
  var MemberListDetailView = Backbone.View.extend({
    
    el: '.centered',
  
    initialize: function() {
      console.log('MemberListDetailView initialize');
    },

    events: { 
      'click #memberlist-delete': 'handleDelete'
    },

    handleDelete: function( ev ) {
      ev.preventDefault();
      var check = confirm("Are you sure you want to delete this Member?");
      if (check == true) {
        this.showLoading()
        var _this = this;
        var data = {memberlist_id: $('#memberlist-id').val()};
        $.ajax({
          url: '/api/memberlists/delete/',
          type: 'POST',
          data: data,
          success: function(data) {
            if (data.redirect) {
              _this.hideLoading();
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

  return MemberListDetailView;

});

    
