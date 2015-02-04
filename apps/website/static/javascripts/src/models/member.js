define([
  'underscore',
  'backbone',
], function(_, Backbone) {
  
  var Member = Backbone.Model.extend({

    default: {
      firstname: null,
      lastname: null,
      email: null,
      slug: null,
      organization: null
    }

  });

  return Member;

});

