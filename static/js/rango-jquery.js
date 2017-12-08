$(document).ready(function () {
    $('#about_btn').click(function (event) {
        $(this).addClass('btn-primary');
        alert('You clicked JQuery on Speed!');
    });

    $('h4').hover(
        function (event) {
            $(this).css('color', 'red');
        },
        function (event) {
            $(this).css('color', 'blue');
        }
    );

    $('.ouch').click(function (event) {
        alert('Ouch');
    });

    $('.search-api').action(
        function (event) {
            url_type = $(this).attr('view');
            params = $(this).attr('params');
            set_action(url_type, params);
        },
        function set_action(url_type, params) {
            if(url_type == 'rango:show_category') {
                $(this).action = '{% url ' + str(url_type) + ' ' + str(params) + ' %}';
            }
            else {
                $(this).action = '{% url ' + str(url_type) + ' %}';
                $('#add_page').hide();
            }
        }
    );
});