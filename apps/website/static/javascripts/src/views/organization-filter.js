define([
  'jquery',
  'underscore',
  'backbone',
  'src/collections/members',
], function($, _, Backbone, MemberCollection) {
  
  var OrganizationFilterView = Backbone.View.extend({

    el: '.send-mail-container',

    members: null,

    filterFields: ['Gender', 'Graduating Class'],

    filterChoices: {
      'Gender': '',
      'Graduating Class': '',
    },

    initialize: function() {
      console.log('OrganizationFilterView initialize');
      var organization_id = $('#organization-id').val();
      this.members = new MemberCollection({'organization_id': organization_id});
      this.members.fetch();
    },

    events: {
      'click #add-filter': 'handleFilter',
    },

    handleFilter: function( ev ) {
      ev.preventDefault();
      this.filterChoices['Gender'] = $('#gender-filter').val();
      this.filterChoices['Graduating Class'] = $('#graduating-class-filter').val();
      this.renderFilteredMembers();
    },

    renderFilteredMembers: function() {
      var _this = this;
      var results = this.members.models;

      results = this.members.filter(function(member) {
        if (_this.filterChoices['Gender'] != '') {
          if (member.get('fields').gender != _this.filterChoices['Gender']) {
            return false;
          }
        }
        return true;
      });
    
      var content = _.template( $('#member-list-template').html(), { Members: results });
      $('#organization-members').html(content);
    }

  });

  return OrganizationFilterView;

});
  
