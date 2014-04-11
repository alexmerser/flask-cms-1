
//Panel class
function SprintPanel(sid, _projects, _list, _form){
	
	var $panel = $('#' + sid);
	var $edit_btn = $panel.find('.z-btn-edit');
	var $new_btn = $panel.find('.z-btn-new');
	var $del_btn = $panel.find('z-btn-del');
	
	var $SprintList = _list;//$('#sprint-list');
	var $SprintForm = _form;//$('#sprint-form');
	var $ProjectList = _projects;
	
	// Get selected sprint id
	// Return -- string type
	function _getSelectedId(){
		var $Row = $SprintList.getSelectedRow();
		return $Row.attr('row_id');
	}
	
	// Set selected sprint id to the form id field
	function _setSelectedId(){
		var $Row = $SprintList.getSelectedRow();
		var sprint_id = $Row.attr('row_id');
		$SprintForm.setFieldByName('id', sprint_id);
		return sprint_id;
	}
	
	var $StartDate = $SprintForm.getFieldByName('start-date');
	var $EndDate = $SprintForm.getFieldByName('end-date');
	
	$StartDate.datepicker({
	    startDate: '-3d'
	})
	
	$EndDate.datepicker({
	    startDate: '-3d'
	})
	
	
	$edit_btn.click(function(){
		var _sid = _getSelectedId();
		
		$.post('/get_sprint', { sid: _sid }).done(
				function(data){
					var fields = $.parseJSON(data.sprint);
					fields['mode'] = 'edit';
					$SprintForm.load(fields);
			});
	});
	
	$new_btn.click(function(){
		$SprintForm.cleanup();
		
		var $Row = $ProjectList.getSelectedRow();
		var project_id = $Row.attr('row_id');
		
		$SprintForm.setFieldByName('project_id', project_id);
		$SprintForm.setFieldByName('mode', 'new');
	});
	
	$del_btn.click(function(){
		var _sid = _getSelectedId();
		$.post('/delete_sprints', { sid: _sid}).done(
				function(data){
					$SprintList.reload($.parseJSON(data.sprints));
			});
	});
	
	
	$('#sprint-form').find('.z-btn-submit').click(function(){
		var values = $SprintForm.getInputValues();
		
		$.post('/submit_sprint', values ).done(
				function(data){
					if (data.errors.length == 0){
						$SprintForm.removeHints();
						$('#sprint_dialog').modal('hide');
						//location.reload();
						var sid = $SprintForm.getFieldByName("project_id").val();
						$.post('/get_sprints', { project_id: sid}).done(
								function(data){
									var _sprints = $.parseJSON(data.sprints);
									$SprintList.reload(_sprints);
									if (_sprints.length > 0){
										$('#project-sprints-tab').find('.z-btn-specs').attr("href","\/sprint_view\/"+ _sprints[0]['id']);
									}
								});
					}else{
						var errors = $.parseJSON(data.errors);
						$SprintForm.showErrors(errors);
					}
				});
	});//End of z-btn-submit click
	
}