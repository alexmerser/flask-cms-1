/*
* Single page form
*/
(function($){
	$.fn.ZForm = function(options){

	// The Form is a single page with following DOM:
	//<form>
	// 	<div class="row form-group" name="name">
	//		<textarea class="form-control z-input" />
	//		<div class="col-md-4 z-label">Name</div>
	// 	</div>
	//</form>
	// Note: The field with z-hint tag will show error message if input is invalid.
	var form = this;
	var $Form = $(this);
	
	
	var settings = $.extend({
			//Default options
			form_id: $(form).attr('id'),
			submit_cb : function(){},
			validationUrl : '',
			height:400}, options);
	
	//Public functions
	this.setMode = function(mode){
		$Form.attr( '_mode', mode );
	}
	
	this.getMode = function(){
		return $Form.attr( '_mode');
	}
	
	this.hide = function(){
		$Form.hide();
	}
	
	this.show = function(){
		if ($Form.is(':hidden'))
			$Form.show();
	}
	
	this.getGroups = function(){
		return $Form.find('div.form-group');
	}

	this.getInputs = function(){
		// Get all jquery objects of the inputs fields to be submit
		return $Form.find('input, select, textarea');
	}
	
	this.getInputValues = function(){
		// Return a dictionary type
		var $Inputs = form.getInputs();
		var ret = {};
		
		$.each($Inputs, function( index, input ) {
			var field = $(input).attr('name');
			var value = $(input).val();
			ret[field] = value;
			});
		
		return ret;
	}
	
	this.removeHints = function(){
		var $Groups = $Form.find('div.form-group');
		
		$.each($Groups, function(index, group){
			_removeHint($(group));
		});
	}
	
	this.showErrors = function(errors){
		$Groups = form.getGroups();
		
		$.each($Groups, function(index, group){
			var input = _getInput($(group));
			var err = _findError( input, errors );
			
			if (err != null){
				_addHint($(group), err['message']);
			}
		});
		
	}
	
	// Load values to the fields
	// Arguments:
	//	values -- dictionary type { field name attribute : value }
	this.load = function(values){
		var $Inputs = form.getInputs();
		
		var inputs = {};
		$Inputs.each(function(index, value){
			var attr = $(this).attr('name');
			inputs[attr] = $(this);
			if(attr in values){
				inputs[attr].val(values[attr]);
			}
		});
	}
	
	this.cleanup = function(values){
		var $Inputs = $Form.find('input, textarea');
		$Inputs.each(function(index, value){
			$(this).val('');
		});
		
		$Form.find('select').each(function(index, value){
			$(this).val("0");
		});
	}
	
	this.setFieldByName = function(name, value){
		$Form.find('[name="'+ name +'"]').val(value);
	}
	
	this.getFieldByName = function(name){
		return $Form.find('[name="'+ name +'"]');
	}
	
	this.submit = function(url, success_callback){
		var mode = form.getMode();
		var _values = form.getInputValues();
		_values['_mode'] = mode;
		
		$.post(url, _values ).done(
				function(data){
					if (data.errors.length == 0){
						form.removeHints();

						success_callback(data);

					}else{
						var errors = $.parseJSON(data.errors);
						form.showErrors(errors);
					}
				});
	}
	
	//Private functions
	function _getInput(group){
		 return group.find('input textarea');
	}
	
	function _addHint(group, hint){
		if (hint != null){
			var $Hint = group.find('div.z-hint');
			if ($Hint){
				$Hint.addClass('z-error-text').text(hint);
			}
		}
	}
	
	function _removeHint(group){
		var $Hint = group.find('div.z-hint');
		if ($Hint){
			$Hint.removeClass('z-error-text').text('');
		}
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
	
	function _getGroup( $Inputbox ){
		// Get the parent Group jQuery object;
		return $Inputbox.closest('.form-group');
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
	
	function _init(){
		
		$Form.height(settings.height);
		form.setMode('new');
		
		//Init click handler for the input control
		//When click the input control the label recovers
		
		$Form.find("input textarea").click(function(event) {
			var $Group = _getGroup( $(this) );
			if($Group){
				_removeHint($Group);
			}
		});
		

		/*
		if(settings.errors == []){
			form.removeHints();
		}else{
			form.showErrors(settings.errors);
		}*/
	}

	
	_init();
	return this;
	
	}//End of ZForm
	
}(jQuery));

