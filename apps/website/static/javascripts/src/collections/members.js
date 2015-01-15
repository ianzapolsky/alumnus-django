define([
  'underscore',
  'backbone',
  'src/models/member',
], function(_, Backbone, Member) {
  
  var Members = Backbone.Collection.extend({

    model: Member,
  
  });

  return Members;

});
