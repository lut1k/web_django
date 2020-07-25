from django import template
from django.db.models import Count, Sum, F
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
