$(document).ready(function () {
    $('#suggestion').keyup(function(){
		var query;
		query = $(this).val();
		$.get('/rango/suggest/', {suggestion: query}, function(data){
			$('#cats').html(data);
		});
	});

    $('#like').click(function (event) {
        var cat_id;
        cat_id = $(this).attr('data-cat-id');
        $.get('/rango/like/', {category_id: cat_id}, function (data) {
            $('#id_count').html(data);
        });
    });

    $('.add_page').click(function (event) {
       var cat_id = $('#like').attr('data-cat-id');
       var url = $(this).attr('data-url');
       var title = $(this).attr('data-title');
       $.get('/rango/add/', {category_id: cat_id, url: url, title: title}, function (data) {
            $('#pages').html(data)
       });
    });
});