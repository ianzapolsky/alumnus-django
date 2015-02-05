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
        var data = {organization_id: $(ev.currentTarget).attr('data-organization-id')};
        $.ajax({
          url: '/api/organizations/delete/',
          type: 'POST',
          data: data,
          success: function (data) {
            console.log(data);
            if (data.redirect) {
              window.location.href = data.redirect;
            }
          }
        });
      }
    }

  });

  return OrganizationListView;

});

    
