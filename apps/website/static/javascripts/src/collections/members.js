define([
  'underscore',
  'backbone',
  'src/models/member',
], function(_, Backbone, Member) {
  
  var Members = Backbone.Collection.extend({

    url: '/api/memberlists/',
    model: Member,
    memberlist_id: null,

    parse: function(data) {
      return JSON.parse(data.members);
    },

    initialize: function(options) {
      this.url += options.memberlist_id;
      this.memberlist_id = parseInt(options.memberlist_id);
    }

  });

  return Members;

});
