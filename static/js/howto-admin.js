(function(){
	$('a#form_submit').on('click', function(){
		var form = $(this).parents('.panel').find('form');
		form.submit();
		return false;
	});
})();