define([
  'underscore',
  'backbone',
  'dist/src/models/member',
], function(_, Backbone, Member) {
  
  var Members = Backbone.Collection.extend({

    url: null,
    model: Member,
    memberlist_id: null,
    memberlist_slug: null,
    organization_id: null,

    parse: function(data) {
      return JSON.parse(data.members);
    },

    initialize: function(options) {
      if (options.memberlist_id) {
        this.url = '/api/memberlists/' + options.memberlist_id;
        this.memberlist_id = parseInt(options.memberlist_id);
      } else if (options.organization_id) {
        this.url = '/api/organizations/' + options.organization_id;
        this.organization_id = parseInt(options.organization_id);
      }
      if (options.memberlist_slug) {
        this.memberlist_slug = options.memberlist_slug;
      }
    }

  });

  return Members;

});
