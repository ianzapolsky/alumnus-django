define([
  'underscore',
  'backbone',
], function(_, Backbone) {
  
  var Member = Backbone.Model.extend({

    default: {
      name: null,
      email: null,
      organization: null
    }
  });

  return Member;

});

