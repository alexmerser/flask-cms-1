
		


function ProjectTree(id, _data){

    
    
    return $Tree;
}


//Panel class
function BacklogPanel(sid, _sprints, _list, _form){
	
	var $panel = $('#' + sid);
	var $edit_btn = $panel.find('.z-btn-edit');
	var $new_btn = $panel.find('.z-btn-new');
	var $del_btn = $panel.find('z-btn-del');
	
	var $BacklogList = _list;//$('#spec-list');
	var $BacklogForm = _form;//$('#spec-form');
	var $SprintList = _sprints;
	
	// Get selected spec id
	// Return -- string type
	function _getSelectedId(){
		var $Row = $BacklogList.getSelectedRow();
		return $Row.attr('row_id');
	}
	
	// Set selected spec id to the form id field
	function _setSelectedId(){
		var $Row = $BacklogList.getSelectedRow();
		var spec_id = $Row.attr('row_id');
		$BacklogForm.setFieldByName('id', spec_id);
		return spec_id;
	}
	
	var $StartDate = $BacklogForm.getFieldByName('start-date');
	var $EndDate = $BacklogForm.getFieldByName('end-date');
	
	$StartDate.datepicker({
	    startDate: '-3d'
	})
	
	$EndDate.datepicker({
	    startDate: '-3d'
	})
	/*
	$edit_btn.click(function(){
		var _sid = _getSelectedId();
		
		$.post('/get_spec', {sid:_sid}).done(
				function(data){
					var fields = $.parseJSON(data.spec);
					fields['mode'] = 'edit';
					$BacklogForm.load(fields);
			});
	});
	
	$new_btn.click(function(){
		$BacklogForm.cleanup();
		
		var $Row = $SprintList.getSelectedRow();
		var sprint_id = $Row.attr('row_id');
		
		$BacklogForm.setFieldByName('sprint_id', sprint_id);
		$BacklogForm.setFieldByName('mode', 'new');
	});
	
	$del_btn.click(function(){
		var _sid = _getSelectedId();
		$.post('/delete_specs', { sid: _sid}).done(
				function(data){
					$BacklogList.reload($.parseJSON(data.specs));
			});
	});
	
	
	$('#spec-form').find('.z-btn-submit').click(function(){
		var values = $BacklogForm.getInputValues();
		
		$.post('/submit_spec', values ).done(
				function(data){
					if (data.errors.length == 0){
						$BacklogForm.removeHints();
						$('#spec_dialog').modal('hide');
						//location.reload();
						var sid = $BacklogForm.getFieldByName("sprint_id").val();
						$.post('/get_specs', { sprint_id: sid}).done(
								function(data){
									var _specs = $.parseJSON(data.specs);
									$BacklogList.reload(_specs);
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
	
	*/
}
