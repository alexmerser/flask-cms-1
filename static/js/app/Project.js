
//Panel class
function ProjectPanel(sid, _list, _form){
	
	var $panel = $('#' + sid);
	var $edit_btn = $panel.find('.z-btn-edit');
	var $new_btn = $panel.find('.z-btn-new');
	var $del_btn = $panel.find('z-btn-del');
	
	var $ProjectList = _list;//$('#project-list');
	var $ProjectForm = _form;//$('#project-form');

	// Get selected project id
	// Return -- string type
	function _getSelectedId(){
		var $Row = $ProjectList.getSelectedRow();
		return $Row.attr('row_id');
	}
	
	// Set selected project id to the form id field
	function _setSelectedId(){
		var $Row = $ProjectList.getSelectedRow();
		var project_id = $Row.attr('row_id');
		$ProjectForm.setFieldByName('id', project_id);
		return project_id;
	}
	
	
	var $StartDate = $ProjectForm.getFieldByName('start-date');
	var $EndDate = $ProjectForm.getFieldByName('end-date');
	
	$StartDate.datepicker({
	    startDate: '-3d'
	})
	
	$EndDate.datepicker({
	    startDate: '-3d'
	})
	
	
	$edit_btn.click(function(){
		var _sid = _getSelectedId();
		
		$.post('/get_project', { sid: _sid }).done(
				function(data){
					var fields = $.parseJSON(data.project);
					fields['mode'] = 'edit';
					$ProjectForm.load(fields);
			});
	});
	
	$new_btn.click(function(){
		$ProjectForm.cleanup();
		$ProjectForm.setFieldByName('mode', 'new');
	});
	
	$del_btn.click(function(){
		var _sid = _getSelectedId();
		$.post('/delete_projects', { sid: _sid}).done(
				function(data){
					$ProjectList.reload($.parseJSON(data.projects));
			});
	});
	
	
}