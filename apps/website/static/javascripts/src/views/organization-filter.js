define([
  'jquery',
  'underscore',
  'backbone',
  'src/collections/members',
], function($, _, Backbone, MemberCollection) {
  
  var OrganizationFilterView = Backbone.View.extend({

    el: '.send-mail-container',

    members: null,

    filters: {},

    initialize: function() {
      console.log('OrganizationFilterView initialize');
      var organization_id = $('#organization-id').val();
      this.members = new MemberCollection({'organization_id': organization_id});
      this.members.fetch();
    },

    events: {
      'change select': 'handleFilter',
    },

    handleFilter: function( ev ) {
      ev.preventDefault();
      this.filters['Gender'] = $('#gender-filter').val();
      this.filters['Graduation Year'] = $('#graduation-year-filter').val();
      this.filters['School'] = $('#school-filter').val();
      this.render();
    },

    render: function() {
      var _this = this;
      var results = this.members.filter(function(member) {
        console.log(member);
        if (_this.filters['Gender'] && member.get('fields').gender != _this.filters['Gender']) {
          return false;
        }
        if (_this.filters['Graduation Year'] && member.get('fields').graduation_year != _this.filters['Graduation Year']) {
          return false;
        }
        if (_this.filters['School'] && member.get('fields').school != _this.filters['School']) {
          return false;
        }
        return true;
      });
    
      var content = _.template( $('#member-list-template').html(), { Members: results });
      $('#organization-members').html(content);
    }

  });

  return OrganizationFilterView;

});
  
