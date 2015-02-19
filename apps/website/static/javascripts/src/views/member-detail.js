define([
  'jquery',
  'underscore',
  'backbone',
], function($, _, Backbone) {
  
  var MemberDetailView = Backbone.View.extend({
    
    el: '#member-detail-container',
  
    initialize: function() {
      console.log('MemberDetailView initialize');
    },

    events: { 
      'click #member-update-request': 'handleUpdateRequest',
      'click #member-delete': 'handleDelete'
    },

    handleUpdateRequest: function( ev ) {
      ev.preventDefault();
      this.showLoading();
      var _this = this;
      var data = {member_id: $('#member-id').val()};
      $.ajax({
        url: '/api/members/request-update/',
        type: 'POST',
        data: data,
        success: function(data) {
          if (data.redirect) {
            _this.hideLoading();
            window.location.replace(data.redirect);
          }
        }
      });
    },

    handleDelete: function( ev ) {
      ev.preventDefault();
      this.showLoading();
      var _this = this;
      var data = {member_id: $('#member-id').val()};
      $.ajax({
        url: '/api/members/delete/',
        type: 'POST',
        data: data,
        success: function(data) {
          if (data.redirect) {
            window.location.replace(data.redirect);
          }
        }
      });
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

    
