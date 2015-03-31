define([
  'underscore',
  'backbone',
], function(_, Backbone) {
  
  var Member = Backbone.Model.extend({

    url: null,

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

