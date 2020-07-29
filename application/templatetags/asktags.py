from django import template
from django.db.models import Count
from application.models import LaskUser, Tag

register = template.Library()


@register.inclusion_tag('include_blocks/best_members.html')
def top_users(*args):
    users = LaskUser.objects.all()[:5]
    return {'users': users}


@register.inclusion_tag('include_blocks/popular_tags.html')
def top_tags(*args):
    tags = Tag.objects.annotate(count=Count('questions')).order_by('-count')[:5]
    return {'tags': tags}


@register.simple_tag
def passes_getparameters_to_new_request(request, *args):
    """
    Attaches filtering and sorting GET parameters to the 'page' parameter of the paginator.
    """
    get_parameters = ''
    for key, value in request.GET.items():
        if key != 'page':
            get_parameters += '&{0}={1}'.format(key, value)
    return get_parameters


