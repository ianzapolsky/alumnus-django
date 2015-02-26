define([
  'jquery',
  'underscore',
  'backbone',
], function($, _, Backbone) {
  
  var MemberListView = Backbone.View.extend({
    
    el: '.member-list-container',

    messages: [],
  
    initialize: function() {
      console.log('MemberListView initialize');
    },

    events: { 
      'click #member-send-mail': 'renderSendMailForm',
    },

    formIsValid: function () {
      var valid = true
      // Check for at least one checked Member
      if ($('input[type=checkbox]:checked').length === 0) {
        this.signalError('Please check at least one Member.');
        this.renderErrors();
        valid = false
      } else {
        this.signalSuccess(); 
      }
      return valid; 
    },

    renderSendMailForm: function () {
      if (this.formIsValid()) {
        var content = _.template( $('#send-mail-template').html());
        $('#send-mail-container').html(content);
      } 
    },

    hideSendMailForm: function () {
      $('#send-mail-container').html('');
    },

    signalError: function(errorMsg) {
      this.messages.push(errorMsg);
    },

    signalSuccess: function() {
      $('#messages-container').html('');
    },

    renderErrors: function() {
      var content = _.template($('#errors-template').html(), {Errors: this.messages});
      $('#messages-container').html(content);
      this.messages = [];
      window.scroll(0,0);
    }

  });

  return MemberListView;

});

    
