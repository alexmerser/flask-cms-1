(function($){
	
	//Example DOM
	//	<ul id="ad-tabs" class="nav nav-tabs z-tabs">
	//		<li class="z-tab" value='rent'><a>{{_('Rental')}}</a></li>
	//		<li class="z-tab" value='sell'><a>{{_('Sell')}}</a></li>
	//	</ul>
	// Note: the value field in <li> is a must
	
	$.fn.ZTab = function(options){
		var settings = $.extend({
			//Default options
			tabClickCallback : null
		}, options);
		
		var $Tab = $(this);
		var tabs = $Tab.find('.z-tab');
		
		this.getActiveTab = function(){
			//Get current active tab under ul.z-tabs
			//Return
			//	jQuery object if success
			return $Tab.find('li.z-tab.active');
		}
		
		this.setActiveTab = function(tab){
			//Arguments:
			//	tab --- jQuery object
			$Tab.find('li.z-tab').removeClass('active');
			tab.addClass('active');
		}
		
		this.showTab = function(tab){
			tab.find('a').tab('show');
		}
		
		this.showTab($(tabs[0]));
		
		return this;
	}//End of ZTab
	
	
	
	//
	//<form class="z-upload-form" action="/preload_image">
	//
	$.fn.ZImageUploader = function(options){
		var settings = $.extend({
			//Default options
			url: "/preload_image",
			get_item_id: function(){return '';},
			preload_done: function(){},
			before_click_cb: function(){},
			pictures:[],
			n_max:4,
			width:108,
			height:108
		}, options);
		
		
		var default_add_new = "../static/images/built_in/default-add-new.jpg";
		var $Uploader = this;
		var $UploadBtn = $Uploader.find('.z-upload-input'); 
		var $Form = $Uploader.find('form.z-upload-form');
		var $Image = $Uploader.find('div.z-thumbnail');
		var $CurrFrame = null;
		
		var _file = null;
		var reader = new FileReader();
		var id = 0;
		var n_items = 0;
		var height = settings.height;
		var width = settings.width;
		var object_id = '';
		
		function _createEmptyFrame(){
		// Create following DOM
		// <li id='z-frame-n'>
		//	<div><input index='n'/></div>
		// </li>
				$Input = $('<input index="' + n_items + '" name="upload-image" class="z-upload-input" type="file" style="opacity:0;"/>').width(width).height(height);
				$Div = $("<div></div>").width(width).height(height).addClass("z-thumbnail").css("background-image","url("+ default_add_new +")").append($Input);
				$Item = $("<li class='col-sm-6 col-md-3'></li>").addClass('z-frame-' + n_items  ).append($Div);
				$Uploader.append($Item);
				n_items++;
		}
		
		function _readURL(input, index) {
			id = index;
			if (input.files){
				_file = input.files[0];
				if (_file) {
					reader.readAsDataURL(_file);
				}
			}
		}

		this.getFileName = function(){
			return _file.name;
		}
		
		for(i=0;i<settings.n_max;i++){
			_createEmptyFrame();
		}
		
		for(i=0; i<settings.n_max; i++){
			$Uploader.find('.z-frame-'+i).find('input').change(function(){
				var index = $(this).attr('index');
				_readURL(this, index);
			});
		}

		reader.onload = function(e) {
					//uploader.css("background-image","url("+ e.target.result +")");
					//uploader.css("background-size", "100px 100px")
					//attr('src', e.target.result);
			settings.before_click_cb();		
			$.post(settings.url, { fname: _file.name, 
								fdata: reader.result,
								oid: settings.get_item_id()}).done(
									function(data){
			        					//update image
			        					$Uploader.find('.z-frame-' + id).find('div').css("background-image","url("+ escape(data.fpath)+")");
			        					$Uploader.find('.z-frame-' + id).find('div').css("background-size", "108px 108px");
			        					object_id = data.oid;
			        					settings.preload_done(data.fname, object_id);
        							});
		}


		

		return this;
		
	}//End of ZTab
	
}(jQuery));