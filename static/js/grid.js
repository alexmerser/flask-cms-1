
/* The Grid class will render an html table:
 * <table class='z-grid'></table>
 * 	
 */
function Grid(options){

	var defaultOptions = {
		selector: null,//jquery selector
		nColumns: 4,
		datas:[],
		getCell: function(data){return ''; },
	}
	
	//Init options
	if( typeof options == 'object'){
		options = $.extend(defaultOptions, options);
	}else{
		options = defaultOptions;
	}
	this.nColumns = options.nColumns;
	selector = options.selector;
	
	// Remove existing grid table
	if( selector.is('not:empty')){
		selector.children('table.z-grid').remove();
	}
	
	tag = '<table class="z-grid"><tr>';
	
	if(typeof(datas) != 'undefined' && datas.length > 0){
		
		for(i=0; i<datas.length; i++){
			tag += '<td>';
			
			//get cell item
			tag += get_cell(datas[i]);
			
			tag += '</td>';
			
			//Change new line
			if((i+1)% nColumns == 0){
				tag += '</tr><tr>';
			}
		}
		
		tag += '</tr></table>';
		selector.append(tag);
	}	
	//Public functions
	
	//Private functions
	function get_cell(data){
		return options.getCell(data);
	}
} 