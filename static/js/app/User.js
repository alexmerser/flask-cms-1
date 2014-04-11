
//Panel class
function UserPanel(sid, _list, _form){
	
	var $panel = $('#' + sid);
	var $edit_btn = $panel.find('.z-btn-edit');
	var $new_btn = $panel.find('.z-btn-new');
	var $del_btn = $panel.find('z-btn-del');
	
	var $UserList = _list;//$('#user-list');
	var $UserForm = _form;//$('#user-form');

	// Get selected user id
	// Return -- string type
	function _getSelectedId(){
		var $Row = $UserList.getSelectedRow();
		return $Row.attr('row_id');
	}
	
	// Set selected user id to the form id field
	function _setSelectedId(){
		var $Row = $UserList.getSelectedRow();
		var user_id = $Row.attr('row_id');
		$UserForm.setFieldByName('id', user_id);
		return user_id;
	}
	
	
	var $StartDate = $UserForm.getFieldByName('start-date');
	var $EndDate = $UserForm.getFieldByName('end-date');
	
	$StartDate.datepicker({
	    startDate: '-3d'
	})
	
	$EndDate.datepicker({
	    startDate: '-3d'
	})
	

	function _getTitleId(title){
        var title_ids = {'Project Manager':'0', 'Team Lead':'1', 'Developer':'2', 'Tester':'3'};
        if(title in title_ids){
        	return title_ids[title];
        }else{
        	return '0';
        } 
	}
	
	function _getRoleId(role){
		var role_ids = {'Admin':'0', 'User':'1'};
        if(role in role_ids){
        	return role_ids[role];
        }else{
        	return '0';
        } 
	}
	
	
	$edit_btn.click(function(){
		var _sid = _getSelectedId();
		
		$.post('/get_user', { sid: _sid }).done(
				function(data){
					var fields = $.parseJSON(data.user);
					fields['mode'] = 'edit';
					fields['role'] = _getRoleId(fields['role']);
					fields['title'] = _getTitleId(fields['title']);
					$UserForm.load(fields);
			});
	});
	
	$new_btn.click(function(){
		$UserForm.cleanup();
		$UserForm.setFieldByName('mode', 'new');
	});
	
	$del_btn.click(function(){
		var _sid = _getSelectedId();
		$.post('/delete_users', { sid: _sid}).done(
				function(data){
					$UserList.reload($.parseJSON(data.users));
			});
	});
	
	
}