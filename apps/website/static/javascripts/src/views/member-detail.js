define([
  'jquery',
  'underscore',
  'backbone',
], function($, _, Backbone) {
  
  var MemberDetailView = Backbone.View.extend({
    
    el: '.member-detail-container',
  
    initialize: function() {
      console.log('MemberDetailView initialize');
    },

    events: { 
      'click #member-request-info': 'handleUpdateRequest',
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
          _this.hideLoading();
          var msg = 'Request sent successfully.';
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

  });

  return MemberDetailView;

});

    
