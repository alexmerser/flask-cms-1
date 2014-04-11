(function($){
	$.fn.ZTable = function(options){
		var settings = $.extend({
			//Default options
			colums:{}, 	// The dictionary contains the pairs like column:column name, for the columns to display
			datas:[],	// The array contains the dictionaries like {column:data}, should have id field, if with_id=true
			with_title: true,
			with_id: true,
			with_checkbox:true,
			select_row_cb: function($Row){},
			row_height: 64,
			row_id: null, // Default selected row_id
			dragable:false,
			bordered:true,
			pagination: true,
            current_page: 0,
            total_pages: 1,
            page_size:5
            
		}, options);
		
		// Initialization
		var holder = this;
		var $Holder = $(this);
		var $Pager = null;
		
		this.checkAll = function(bCheck){
			// Check,Uncheck all the check boxes
			var checkboxes = $Holder.find("input[type='checkbox']");
			
			$.each(checkboxes,function(index, checkbox){
				$(checkbox).prop('checked', bCheck);
			});
		}
		this.checkRows = function(_ids, bCheck){
			var $Rows = $Holder.find('tbody').find('tr');
			$.each($Rows, function(index, row){
				
				if(_ids.indexOf($.data($(row),'id')) != -1){
					var $Checkbox = $(row).find("input[type='checkbox']");
					$Checkbox.prop('checked', bCheck);
				}
			});
			return _ids;
		}
		this.getCheckedRows = function(){
			// Get tr rows which was checked
			var $Rows = $Holder.find('tbody').find('tr');
			var _rows = [];
			$.each($Rows, function(index, row){
				if($(row).find("input[type='checkbox']").is(':checked')){
					_rows.push($(row));
				}
			});
			return _rows;
		}
		
		this.getCheckedIds = function(){
			var $Rows = $Holder.find('tbody').find('tr');
			var _ids = [];
			$.each($Rows, function(index, row){
				var $Checkbox = $(row).find("input[type='checkbox']");
				if($Checkbox.is(':checked')){
					_ids.push($(row).data('id'));
				}
			});
			return _ids;
		}
		
		this.showRows = function(_ids){
			var $Rows = $Holder.find('tbody').find('tr');
			$.each($Rows, function(index, row){
				if(_ids.indexOf($(row).data('id')) != -1){
					$(row).show();
				}
			});
			return _ids;
		}
		
		
		this.getPageSize = function(){
			return settings.page_size;
		}
		
		this.getMode = function(){
			return this.attr('mode');
		}
		
		this.setMode = function(mode){
			//Argument:
			// mode --- 'normal' or 'edit'
			return this.attr('mode', mode);
		}
		
		this.getSelectedRow = function(){
			return $(this).find('.highlight');
		}
		

		
		this.selectRow = function($Row){
			$Holder.find('tbody').find('tr').removeClass('highlight');
			$Row.addClass('highlight');
			/*
			if(settings.with_checkbox){
		     	$checkbox = $Row.find("input[type='checkbox']");
		    	if($checkbox.is(':checked')){
		    		$checkbox.prop('checked', false);
		    	}else{
		    		$checkbox.prop('checked', true);
				}
			}
			*/
		    settings.select_row_cb( $Row );
		}
		
		this.appendRow = function(row){
			this.find('tbody').append(row);
		}
		
		
		this.loadAll = function(datas, columns){
			settings.datas = datas;
			holder.loadHead(columns);
			holder.loadData(datas);
			
			$Holder.find( "thead input[type='checkbox']").click( function(event) {
				if($(this).is(':checked')){
					holder.checkAll(true);
				}else{
					holder.checkAll(false);
				}
			});
			
			
		}
		
		this.showPage = function(page_index){
			settings.current_page = page_index;
			var total = settings.datas.length;
			if(settings.pagination){
				if(total != 0){
					var pos = paginate(total, settings.current_page);
					var rows = $Holder.find('tbody').find('tr');
					
					for(var i=0; i<pos['start'];i++){
						$(rows[i]).hide();
					}
					for(var i=pos['start']; i<pos['end']; i++){
						$(rows[i]).show();
					}
					for(var i=pos['end']; i<total; i++){
						$(rows[i]).hide();
					}
				}
			}else{
				var rows = $Holder.find('tbody').find('tr');
				for(var i=0; i<total; i++){
					$(rows[i]).show();
				}
			}
		}
		
		this.reload = function(datas, columns, current_page){
			// Reload will lost current status like checkbox
			settings.datas = datas;
			settings.current_page = current_page;
			
			holder.loadHead(columns);
			
			if(settings.pagination){
				if(datas.length != 0){
					var pos = paginate(datas.length, settings.current_page);
					holder.loadData(datas, pos['start'], pos['end']);
				}else{
					holder.loadData(datas);
				}
			}else{
				holder.loadData(datas);
			}
		}
		
		this.loadHead = function(columns){
			var $Head = $Holder.find('thead');
			var $HeadRow = $('<tr></tr>');
			
			if(settings.with_checkbox){
				$HeadRow.append('<th><input type="checkbox"></th>');
			}
			
			for(var key in columns){
				$HeadRow.append('<th>'+ columns[key] +'</th>');
			}
			$Head.empty().append($HeadRow);
		}
		
		function paginate(total, page_index){
			
			settings.total_pages = Math.floor((total - 1) / settings.page_size) + 1;
			
			if (page_index < settings.total_pages - 1 ){
				return {'start' : page_index * settings.page_size,
					'end' : page_index * settings.page_size + settings.page_size};
			}else if(page_index == settings.total_pages -1){
				return {'start' : page_index * settings.page_size,
						'end' : total};
			}else{
				//Error
			}
		}
		
		this.loadData = function( datas, start, end){
			var $Body = $Holder.find('tbody').empty();
			var start = typeof start !== 'undefined' ? start : 0;
			var end = typeof end !== 'undefined' ? end : datas.length;
			if(datas.length != 0){
				for(var i=start; i<end; i++){
					var $Row = $('<tr></tr>');
					
					if(settings.with_id){
						//$Row.attr('row_id', datas[i]['_id']);
						$Row.data('id', datas[i]['_id']);
					}
					
					if(settings.with_checkbox){
						$Row.append('<td><input type="checkbox"></td>');
					}
	
					for(var key in settings.columns){
						$Row.append('<td>'+ datas[i][key] +'</td>');
					}
					$Body.append($Row);
				}
			}
			// Select the first row by default
			if (settings.row_id == null){
				holder.selectRow($Holder.find( 'tbody > tr:first'));
			}else{
				row = $Table.getRow(settings.row_id);
				if (row != null)
					holder.selectRow(row);
				else
					holder.selectRow($Table.find( 'tbody > tr:first'));
			}
			
			$Holder.find('tbody > tr').click(function(){
				holder.selectRow($(this));
			});
			
		}
		
		this.createTable = function(){
			// Create an empty table
			var $Table = $('<table></table>').addClass("table table-hover table-responsive").empty();
			
			$Table.append('<thead></thead>').append('<tbody></tbody>');
				
			
			if(settings.bordered){
				$Table.addClass("table-bordered");
			}
			
			$Holder.empty().append($Table);
			
			if(settings.pagination){
				$Holder.append($('<div></div>').addClass('z-pagination row col-sm-8 pull-right'));
			}
		}
		
		this.updatePagination = function(){
			datas = settings.datas;
			if(datas.length != 0){
				
				var pageSize = holder.getPageSize();
				var totalPages = Math.floor((datas.length - 1) / pageSize) + 1;
				
				$Pager = $Holder.find('.z-pagination').bootstrapPaginator({
		            currentPage: 1,
		            totalPages: totalPages,
		            numberOfPages:5,
		            onPageClicked: function(e,originalEvent,type,page){
		            	holder.showPage(page-1);
		            }
		        });
			}
		}
		
		this.createTable2 = function(){
			var $Table = $('<table></table>');
			
			
			var columns = settings.columns;
			var datas = settings.datas;
			
			// Create header
			var $Head = $('<thead></thead>');
			loadHead($Head, columns);
			
			// Create body
			var $Body = $('<tbody"></tbody>');
			if(settings.pagination){
				var pos = paginate(datas.length, settings.current_page);
				holder.loadData($Body, datas, pos['start'], pos['end']);
			}else{
				holder.loadData($Body, datas);
			}
			$Table.addClass("table table-hover table-responsive").empty();
			
			if(settings.bordered){
				$Table.addClass("table-bordered");
			}
			
			if(settings.with_title){
				$Table.prepend($Head)
			}
			
			$Table.append($Body);
			$Holder.empty().append($Table);
			
			// Set row select handler
			/*
			$Table.find( 'tbody > tr').click( function(event) {
			    if (event.target.type == 'checkbox'){
			    	$(this).addClass('highlight').siblings().removeClass('highlight');
			    	event.stopPropagation();
			    	settings.select_row_cb( $(this) );
			    }else{
			    	holder.selectRow($(this));
			    } 	
			});
			*/
			
			// Set checkbox handler
			/*
			$Table.find('input[name="selected"]:checked').click(function(){
				$(this).prop('checked', false);	
			});
			*/
			// Set height
			//$Table.find( 'tbody > tr').height(settings.height);
		}// End of create
		

		// Return dictionary
		this.getRowData = function(id){
			var datas = settings.datas;
			for(var i=0; i<datas.length; i++){
				if(datas[i]['id'] == id){
					// clone object
					return $.extend({}, datas[i]);
				}
			}
			return {};
		}
		
		this.getRow = function(row_id){
			rows = $Holder.find( 'tbody > tr');
			for(var i=0; i<rows.length; i++){
				if ($.data($(rows[i]),'id') == row_id){
					return $(rows[i]);
				}
			}
			return null;
		}
		
		this.clear = function(){
			$(this).find('tbody').empty();
		}
		
		this.createTable();
		if (settings.datas.length != 0)
			this.reload(settings.datas, settings.columns, settings.current_page);

		
		return this;

	}//End of ZTable
	
}(jQuery));
