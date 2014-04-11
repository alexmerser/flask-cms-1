
//Panel class
function SpecPanel(sid, _sprints, _list, _form){
	
	var $panel = $('#' + sid);
	var $edit_btn = $panel.find('.z-btn-edit');
	var $new_btn = $panel.find('.z-btn-new');
	var $del_btn = $panel.find('z-btn-del');
	
	var $SpecList = _list;//$('#spec-list');
	var $SpecForm = _form;//$('#spec-form');
	var $SprintList = _sprints;
	
	// Get selected spec id
	// Return -- string type
	function _getSelectedId(){
		var $Row = $SpecList.getSelectedRow();
		return $Row.attr('row_id');
	}
	
	// Set selected spec id to the form id field
	function _setSelectedId(){
		var $Row = $SpecList.getSelectedRow();
		var spec_id = $Row.attr('row_id');
		$SpecForm.setFieldByName('id', spec_id);
		return spec_id;
	}
	
	var $StartDate = $SpecForm.getFieldByName('start-date');
	var $EndDate = $SpecForm.getFieldByName('end-date');
	
	$StartDate.datepicker({
	    startDate: '-3d'
	})
	
	$EndDate.datepicker({
	    startDate: '-3d'
	})
	
	$edit_btn.click(function(){
		var _sid = _getSelectedId();
		
		$.post('/get_spec', {sid:_sid}).done(
				function(data){
					var fields = $.parseJSON(data.spec);
					fields['mode'] = 'edit';
					$SpecForm.load(fields);
			});
	});
	
	$new_btn.click(function(){
		$SpecForm.cleanup();
		
		var $Row = $SprintList.getSelectedRow();
		var sprint_id = $Row.attr('row_id');
		
		$SpecForm.setFieldByName('sprint_id', sprint_id);
		$SpecForm.setFieldByName('mode', 'new');
	});
	
	$del_btn.click(function(){
		var _sid = _getSelectedId();
		$.post('/delete_specs', { sid: _sid}).done(
				function(data){
					$SpecList.reload($.parseJSON(data.specs));
			});
	});
	
	// For sprint_view.html
	$('#spec-form').find('.z-btn-submit').click(function(){
		var values = $SpecForm.getInputValues();
		
		$.post('/submit_spec', values ).done(
				function(data){
					if (data.errors.length == 0){
						$SpecForm.removeHints();
						$('#spec_dialog').modal('hide');
						//location.reload();
						var sid = $SpecForm.getFieldByName("sprint_id").val();
						$.post('/get_specs', { sprint_id: sid}).done(
								function(data){
									var _specs = $.parseJSON(data.specs);
									$SpecList.reload(_specs);
									if (_specs.length > 0){
										$('#sprint-specs-tab').find('.z-btn-specs').attr("href","\/spec_view\/"+ _specs[0]['id']);
									}
								});
					}else{
						var errors = $.parseJSON(data.errors);
						$SprintForm.showErrors(errors);
					}
				});
	});//End of z-btn-submit click
}