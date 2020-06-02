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

    $('a.like').click(function (event) {
        event.preventDefault()
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
                } else if (data['status'] === 'error' && data['code'] === 'no_auth') {
                    // TODO допилить всплывающее окно
                    return NaN;
                }
            }
        )
    })

    $('a.correct-answer').click(function (event) {
        event.preventDefault()
        $.post(
            "/correct_answer/",
            {question_id: $(this).data('question_id'), answer_id: $(this).data('answer_id')},
            function (data) {
                if (data['status'] === 'ok') {
                    const correct_answer_id = data['correct_answer_id']
                    $('i.fas.fa-check').addClass("d-none")
                    $('a.correct-answer i').removeClass('far fa-check-square').addClass('far fa-square');
                    $('a.correct-answer.' + correct_answer_id + ' i').removeClass('far fa-square').addClass('far fa-check-square');
                }
            }
        )
    })
});


