define([
  'jquery',
  'underscore',
  'backbone',
], function($, _, Backbone) {
  
  var MemberCreateView = Backbone.View.extend({
    
    el: '#form-container',

    maxFieldset: 1,
    currentFieldset: 0,
    
  
    initialize: function() {
      console.log('GenericFormView initialize');
      this.renderMultistepFormHeader();
      this.renderCurrentFieldset(); 
    },

    events: { 
      'keydown input[type=text]': 'removeRequiredError',
      'keydown input[type=email]': 'removeRequiredError',

      'click #btn-back': 'handleBack',
      'click #btn-next': 'handleNext',
      
      'change #id_email': 'validateEmail',
      'click #btn-submit': 'checkRequired',
      'click #next': 'renderNextFieldset',

    },

    handleBack: function (ev) {
      ev.preventDefault();
      this.currentFieldset -= 1;
      this.renderMultistepFormHeader();
      this.renderCurrentFieldset(); 
    },

    handleNext: function (ev) {
      ev.preventDefault();
      if (this.validateRequired()) {
        this.currentFieldset += 1;
        this.renderMultistepFormHeader();
        this.renderCurrentFieldset(); 
      }
    },

    renderMultistepFormHeader: function () {
      var _this = this;
      _.forEach($('.multistep-form-header').find('li'), function (node, index) {
        if (index == _this.currentFieldset)
          $(node).addClass('active');
        else 
          $(node).removeClass('active');
      });
    },

    renderCurrentFieldset: function () {
      var _this = this;
      _.forEach($('fieldset'), function (node) {
        if ($(node).attr('data-index') != _this.currentFieldset)
          $(node).addClass('hidden');
        else
          $(node).removeClass('hidden');
      });
      if (this.currentFieldset == this.maxFieldset) {
        $('#btn-submit').removeClass('hidden');
        $('#btn-next').addClass('hidden');
      } else {
        $('#btn-submit').addClass('hidden');
        $('#btn-next').removeClass('hidden');
      }
      if (this.currentFieldset == 0)
        $('#btn-back').addClass('hidden');
      else
        $('#btn-back').removeClass('hidden');
    }, 
        
    removeRequiredError: function (ev) {
      if ($(ev.currentTarget).val() != '') {
        $(ev.currentTarget).parent().removeClass('has-error');
        $(ev.currentTarget).tooltip('destroy');
      }
    },

    validateRequired: function() {
      var _this = this;
      var valid = true;
      _.forEach($('input,textarea,select').filter('[required]:visible'), function(field) {
        var field = $(field);
        if (field.val() === '') {
          valid = false;
          _this.signalError(field, 'This field is required.');
        }
      });
      return valid;
    },

    checkRequired: function (ev) {
      ev.preventDefault();
      if (this.validateRequired())
        $('form').submit();
    },

    validateEmail: function() {
      var $email = $('#id_email');
      var x = $email.val();
      var atpos = x.indexOf("@");
      var dotpos = x.lastIndexOf(".");
      if (atpos< 1 || dotpos<atpos+2 || dotpos+2>=x.length) {
        this.signalError($email, 'Not a valid e-mail address.');
      } else {
        this.signalSuccess($email);
      }
    },


    signalError: function($container, errorMsg) {
      $container.parent().removeClass('has-success');
      $container.parent().addClass('has-error');
      $container.tooltip({'trigger': 'manual', 'placement': 'bottom', 'title': errorMsg}).tooltip('show');
    },

    signalSuccess: function($container) {
      $container.parent().removeClass('has-error');
      $container.parent().addClass('has-success');
      $container.tooltip('destroy');
    }

  });

  return MemberCreateView;

});

    
