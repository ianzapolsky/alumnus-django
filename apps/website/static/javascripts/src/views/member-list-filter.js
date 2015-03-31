define([
  'jquery',
  'underscore',
  'backbone',
  'dist/src/collections/members',
], function($, _, Backbone, MemberCollection) {
  
  var MemberListFilterView = Backbone.View.extend({

    el: '.member-list-container',

    members: null,

    ascending: true,

    filters: {},
    
    initialize: function() {
      console.log('MemberListFilterView initialize');
      var organization_id = $('#organization-id').val();
      this.members = new MemberCollection({'organization_id': organization_id});
      this.members.fetch();
    },

    events: {
      'change .filter-select': 'handleFilter',
      'click input[type=radio]': 'changeOrder',
    },

    changeOrder: function ( ev ) {
      if ($(ev.currentTarget).val() === 'asc')
        this.ascending = true;
      else
        this.ascending = false;
      this.render();
    },

    handleFilter: function( ev ) {
      ev.preventDefault();
      this.filters['Sort'] = $('#sort-filter').val();
      this.filters['Participant Type'] = $('#participant-type-filter').val();
      this.filters['Graduation Year From'] = $('#graduation-year-from-filter').val();
      this.filters['Graduation Year To'] = $('#graduation-year-to-filter').val();
      this.filters['School'] = $('#school-filter').val();
      this.filters['Current State'] = $('#state-filter').val();
      this.filters['Industry'] = $('#industry-filter').val();
      this.filters['Gender'] = $('#gender-filter').val();
      this.render();
    },

    render: function() {
      var _this = this;
      var results = this.members.filter(function(member) {
        if (_this.filters['Participant Type'] && member.get('fields').participant_type != _this.filters['Participant Type']) {
          return false;
        }
        if (_this.filters['Gender'] && member.get('fields').gender != _this.filters['Gender']) {
          return false;
        }
        // both year inputs are filled out
        if (_this.filters['Graduation Year From'] && _this.filters['Graduation Year To']) {
          var grad = parseInt(member.get('fields').graduation_year);
          var from = parseInt(_this.filters['Graduation Year From']);
          var to = parseInt(_this.filters['Graduation Year To']);
          if (isNaN(grad))
            return false;
          else if (grad < from || grad > to)
            return false;
        }
        if (_this.filters['School'] && member.get('fields').school != _this.filters['School']) {
          return false;
        }
        if (_this.filters['Current State'] && member.get('fields').current_state != _this.filters['Current State']) {
          return false;
        }
        if (_this.filters['Industry'] && member.get('fields').industry != _this.filters['Industry']) {
          return false;
        }
        return true;
      });

      if (this.filters['Sort']) {
        var results = _.sortBy(results, function(member) {
          var func = "member.get('fields')." + _this.filters['Sort'];
          return eval(func);
        });
      }

      if (this.filters['Sort'] && !this.ascending)
        results.reverse();
  
      // Reverse to match expected behavior for alphabetical sorting.
      if (this.filters['Sort'] === 'firstname' || this.filters['Sort'] === 'lastname')
        results.reverse();
    
      var content = _.template( $('#member-list-template').html(), { Members: results });
      $('#member-list-members').html(content);
    }

  });

  return MemberListFilterView;

});
  
