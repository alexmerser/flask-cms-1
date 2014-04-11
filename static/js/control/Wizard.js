function Wizard(options){
	// The Wizard has following DOM:
	// <div class="row form-group" name="name">
	//	<textarea class="form-control z-input" />
	//	<div class="col-md-4 z-label">Name</div>
	// </div>
	
	var wizard = this;
	var settings = $.extend({
			//Default options
			form_id: 'z-form',
			validationUrl : '',
			height:400,
		}, options);
	
	var $Form = $('#' + settings.form_id);
	var labels = _getDefaultLabels();
	var	multiPages = null;
	
	this.hide = function(){
		$Form.hide();
	}
	this.show = function(){
		$Form.show();
	}
	this.getGroups = function(pageIndex){
		var $Page = $Form.find('div.z-page[value="'+ pageIndex +'"]');
		return $Page.find('div.form-group');
	}

	this.getValidationInputs = function(pageIndex){
		// Get inputs to be send to backend for validation
		var $Page = $Form.find('div.z-page[value="'+ pageIndex +'"]');
		
		var inputs = $Page.find('.z-input');
		var ret = {'page': pageIndex.toString()};
		
		$.each(inputs, function( index, input ) {
			var field = $(input).attr('name');
			var value = $(input).val();
			ret[field] = value;
			});
		
		return ret;
	}
	
	function _getDefaultLabels(){
		var $Groups = $Form.find('div.form-group');
		var labels = new Array();
		
		$.each($Groups, function(index, group){
			var name = $(group).attr('name');
			var label = $(group).find('div.z-label').text();
			
			labels[name] = label;
		});
		
		return labels;
	}
	
	function _setControlName(){
		// Add name attribute to the '.form-control' fields
		var $Groups = $Form.find('div.form-group');
		
		$.each($Groups, function(index, group){
			var name = $(group).attr('name');
			var $Control = $(group).find('.form-control');
			$Control.attr('name', name );
		});
	}
	
	function _init(){
		_setControlName();
		
		//Init click handler for the input control
	
		$Form.find(".z-input").click(function(event) {
			var $Group = _getGroup( $(this) );
			var name = $Group.attr('name');
			var $Label = $Group.find('.z-label');
			
			$Label.removeClass('z-error-text').addClass('z-text').text(labels[name]);
		});
		
		
		multiPages = $Form.ZMultiPages({
			height:settings.height,
			validationUrl : settings.validationUrl,
			getValidationInputs:wizard.getValidationInputs,
			showErrors:wizard.showErrors,
			resetLabels:wizard.resetLabels});
	}
	
	
	function _findError( input, errors ){
		// Find if there's error in the back end errors array
		//Arguments:
		// input -- jquery object
		var name = $(input).attr('name');
		for( var index in errors)
			if( errors[index]['field'] == name)
				return errors[index];
		return null;
	}
	
	this.resetLabels = function(){
		var $Groups = $Form.find('div.form-group');
		
		$.each($Groups, function(index, group){
			var name = $(group).attr('name');
			var $Label = $(group).find('.z-label');
			$Label.removeClass('z-error-text').addClass('z-text').text(labels[name]);
		});
	}
	
	this.showErrors = function(errors, pageIndex){
		$Groups = wizard.getGroups(pageIndex);
		
		$.each($Groups, function(index, group){
			var input = $(group).find('.z-input');
			
			var err = _findError( input, errors );
			
			if (err != null){
				var $Label = $(group).find('div.z-label').text(err['message']);
				$Label.removeClass('z-text').addClass('z-error-text');
			}
		});
		
	}
	
	function _getGroup( inputbox ){
		var name = inputbox.attr('name');
		return $Form.find('div.form-group[name="' + name + '"]');
	}
	
	_init();
}
