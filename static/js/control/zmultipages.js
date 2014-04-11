
(function($){
/*
* Multiple page form,
* The form should have z-group .z-prev-btn, .z-next-btn, .z-submit-btn, z-page, z-title
* Example:
*	<div class="row form-group">
* 		<div id="basic-info" class="z-page" value="1">
*/
	$.fn.ZMultiPages = function(options){
		var form = this;
		
		var settings = $.extend({
			validationUrl : '',
			height:400,
			getPages : function(){return form.find('.z-page');},
			getValidationInputs : function(){return {};},
			showErrors: function(errors){},
			resetLabels: function(){}
		}, options);

		// Initialization
		var pages = settings.getPages();
		var prev_btn = this.find('.z-prev-btn');
		var next_btn = this.find('.z-next-btn');
		var submit_btn = this.find('.z-submit-btn');
		
		//this.hide();
		

		
		
		//Reload pages 
		// Arguments:
		// 	getPagesCallback --- the callback to get pages
		this.reload = function(getPagesCallback){
			if(typeof(getPagesCallback)!= 'undefined'){
				settings.getPages = getPagesCallback;
				pages = settings.getPages();
			}
		}
		
		this.show = function(){
			if (this.is(':hidden'))
				this.slideDown(300);
		}
		
		this.setTitle = function(title){
			this.find('div.z-title > h3').text(title)
		}
				
		this.setAction = function(action){
			this.find('input[name="action"]').val(action);
		}
		
		this.getPage = function(index){
		//Argument:
		// index-- start from 0
			if (index < pages.length-1)
				return $(pages[index])
			else
				return null
		}
		

		
		
		function _getActivePage(){
			for(i=0; i<pages.length; i++){
				if ($(pages[i]).is(":visible")){
					return i;
				}
			}
			return null;
		}

		function _moveToPage(from, to){
			if ( to >= 0 && to < pages.length ){
				if ( from >=0 && from < pages.length ){
					$(pages[from]).hide();
				}
				$(pages[to]).show();
			}
		}
		
		function _moveToNextPage(){
			n = _getActivePage();
			if(! _atLastPage(n)){
				_moveToPage(n, n+1);
				if (_atLastPage(n+1)){
					next_btn.hide();
					submit_btn.show();
				}
				prev_btn.show();
			}
		}
		
		function _moveToPrevPage(){
			n = _getActivePage();
			if(! _atFirstPage(n)){
				_moveToPage(n, n-1);
				if (_atFirstPage(n+1)){
					prev_btn.hide();

				}
				next_btn.show();
				submit_btn.hide();
			}
		}
		
		function _atFirstPage(index){
			return index == 0;
		}
		
		function _atLastPage(index){
			return index == pages.length-1;
		}
		
		
		
		// Set prev button handler
		prev_btn.click(function(){
			_moveToPrevPage();
		});

		/*
		// Set next button handler
		next_btn.click(function(){
		
			// validate current page
			var errors = settings.validate()
			if( errors == [] ){
				
			}else{
				settings.show_errors(errors);
			}
		
			n = _getActivePage();
			
			if(! _atLastPage(n)){
				_moveToPage(n, n+1);
				if (_atLastPage(n+1)){
					submit_btn.show();
				}
			}
		});
		*/
		
		// Set next button handler
		next_btn.click(function(){
			var url  = settings.validationUrl;
			var index = _getActivePage();
			var data = settings.getValidationInputs(index);
			

			// Do backend validation through ajax					
			$.post(url, data).done(function(d){
				if(d.errors.length == 0){
					settings.resetLabels();
					_moveToNextPage();
				}else{
					settings.showErrors(d.errors, index);
				}
			});//end of .done
		});//end of next_btn.click
		
		// Init
		if (pages.length==1){
			prev_btn.hide();
			next_btn.hide();
			submit_btn.show();
		}else{
			prev_btn.hide();
			next_btn.show();
			submit_btn.hide();
		}
		
		form.find('.z-page').height(settings.height);
		form.find('.z-page[value!="0"]').hide();
		
		return this;

	}//End of ZMultiPages
	
}(jQuery));