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
        e.preventDefault()
        $.post(
            "/like/",
            {id: $(this).data('id'), action: $(this).data('action'), type: $(this).data('type')},
            function (data) {
                if (data['status'] === 'ok'){
                    const id_obj_like = data['id_obj_like'];
                    let previous_action = $('a.like.' + id_obj_like).data('action');
                    let total_likes = data['like_count']
                    if (previous_action === 'like') {
                        $('a.like.' + id_obj_like).data('action', 'unlike');
                        $('a.like.' + id_obj_like + ' i').removeClass('far fa-heart').addClass('fas fa-heart')
                        $('span.' + id_obj_like).text(total_likes);
                    } else {
                        $('a.like.' + id_obj_like).data('action', 'like');
                        $('a.like.' + id_obj_like + ' i').removeClass('fas fa-heart').addClass('far fa-heart');
                        $('span.' + id_obj_like).text(total_likes);
                    }
                }
            }
        )
    })
});


