define([
  'jquery',
  'underscore',
  'backbone',
], function($, _, Backbone) {
  
  var OrganizationListView = Backbone.View.extend({
    
    el: '#organization-container',
  
    initialize: function() {
      console.log('OrganizationListView initialize');
    },

    events: { 
      'click .organization-delete': 'handleDelete'
    },

    handleDelete: function (ev) {
      ev.preventDefault();
      var check = confirm("Are you sure you want to delete this Organization?");
      if (check == true) {
        this.showLoading();
        var _this = this;
        var data = {organization_id: $(ev.currentTarget).attr('data-organization-id')};
        $.ajax({
          url: '/api/organizations/delete/',
          type: 'POST',
          data: data,
          success: function (data) {
            _this.hideLoading();
            if (data.redirect) {
              window.location.href = data.redirect;
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

  return OrganizationListView;

});

    
