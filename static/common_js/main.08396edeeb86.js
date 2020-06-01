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
        e.preventDefault();
        $.post(
            // TODO изменить потом question -> object
            '{% url "application:like" %}', {object: $(this).data('question'), action: $(this).data('action')},
            function (data) {
                if (data['status'] == 'ok'){
                    let previous_action = $('a.like').data('action');
                    //    Изменяю переменную действия.
                    $('a.like').data('action', previous_action == 'like' ? 'unlike' : 'like');
                }
            }
        )
    })
});


