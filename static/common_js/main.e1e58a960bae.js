const csrftoken = Cookies.get('csrftoken');

function csrfSafeMethod(method) {
    // Для этих методов токен не будет подставляться в заголовок.
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


$(document).ready(function(){
    $('#id_avatar').removeClass('form-control').addClass('form-control-file');
    $('a.like').click(function (e) {
        //TODO реализовать call-back функцию
        // e.preventDefault()
        $.post(
            "/like/",
            {id: $(this).data('id'), action: $(this).data('action'), type: $(this).data('type')},
            function (data) {
                if (data['status'] == 'ok'){
                    let previous_action = $('a.like').data('action');

                    // Изменяю переменную действия.
                    $('a.like').data('action', previous_action == 'like' ?'unlike' : 'like');
                }
            }
        )
    })
});


