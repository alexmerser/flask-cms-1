(function($){
	$.fn.ZTree = function(options){

	// The Form is a single page with following DOM:
	//<form>
	// 	<div class="row form-group" name="name">
	//		<textarea class="form-control z-input" />
	//		<div class="col-md-4 z-label">Name</div>
	// 	</div>
	//</form>
	// Note: The field with z-hint tag will show error message if input is invalid.
	var tree = this;
	
	var settings = $.extend({
			//Default options
			id: $(tree).attr('id'),
			data : [],
			onUpdate: function(node){},
			onOpen:function(node){},
			onClose:function(node){},
			onClick:function(node){}
			}, options);
	
	
    this.element = $('#' + settings.id).tree({
        data: settings.data,
        selectable: true,
        saveState:true,
        autoEscape: false,
        //autoOpen: true
        //openedIcon: '-',
        //closedIcon: '+'
    });
     
    var $Tree = this.element;
    
    this.getSelectedNode = function(){
    	return $Tree.tree('getSelectedNode');
    }
    
    this.loadData = function(_data){
    	$Tree.tree('loadData', _data);
    	
    	var root = $Tree.tree('getNodeById', "0");
    	if(root.children.length > 0){
    		var node = root.children[0];
    		$Tree.tree('selectNode', node);
    		$Tree.tree('openNode', node);
    		settings.onUpdate(node);
    	}else{
    		$Tree.tree('selectNode', root);
    		$Tree.tree('openNode', root);
    		settings.onUpdate(root);
    	}
    }
    

	
	$Tree.bind('tree.open',
		    function(e) {
		        //console.log(e.node);
		    	//$ProjectTree.tree('openNode', root);
		    }
		);
	$Tree.bind('tree.close',
		    function(e) {
		        //console.log(e.node);
		    }
		);
	
	$Tree.bind('tree.click',
	    function(e) {
	        // The clicked node is 'event.node'
	        var node = e.node;
	        settings.onUpdate(node);
	    }
	);
	
	
	return this;
	
	}//End of ZTree
	
}(jQuery));