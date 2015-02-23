define([
  'jquery',
  'underscore',
  'backbone',
  'src/models/member',
  'src/collections/members',
], function($, _, Backbone, MemberModel, MemberCollection) {
  
  var MemberlistListView = Backbone.View.extend({
    
    el: '#memberlist-container',

    memberlists: [],
  
    initialize: function() {
      console.log('MemberlistListView initialize');
      var _this = this;
      _.forEach($('.memberlist-id'), function(node) {
        var memberlist_id = $(node).val();
        var memberlist_slug = $(node).next().val();
        _this.memberlists.push(new MemberCollection({'memberlist_id': memberlist_id, 'memberlist_slug': memberlist_slug}));
      });
      _.forEach(this.memberlists, function(memberlist) {
        memberlist.fetch();
      });
    },

    events: { 
      'click .memberlist-link': 'renderMemberlist'
    },

    renderMemberlist: function( ev ) {
      ev.preventDefault();
      var memberlist_id = $(ev.currentTarget).attr('data-memberlist-id');
      var memberlist = _.find(this.memberlists, function(memberlist) {
        return memberlist.memberlist_id === parseInt(memberlist_id);
      });
      var content = _.template( $('#member-list-template').html(), { Members: memberlist });
      $('#memberlist-members').html(content);
    },

  });

  return MemberlistListView;

});

    
