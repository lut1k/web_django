from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse

from .models import Like


# Functions for implementing likes.
User = get_user_model()


def add_like(obj, user):
    """Add a like to an `obj`.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    like, is_created = Like.objects.get_or_create(
        content_type=obj_type,
        object_id=obj.id,
        user=user,
    )
    return like


def remove_like(obj, user):
    """Remove a like from an `obj`.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    Like.objects.filter(
        content_type=obj_type,
        object_id=obj.id,
        user=user,
    ).delete()


def is_fan(obj, user) -> bool:
    """Check whether a user liked an `obj` or not.
    """
    if not user.is_authenticated:
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    likes = Like.objects.filter(
        content_type=obj_type,
        object_id=obj.id,
        user=user,
    )
    return likes.exists()


def get_fans(obj):
    """Get the users which liked an `obj`.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    return User.objects.filter(
        likes__content_type=obj_type,
        likes__object_id=obj.id
    )


# common decorators


def login_required_ajax(view):
    def view2(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view(request, *args, **kwargs)
        elif request.is_ajax():
            return JsonResponse({'status': 'error',
                                 'code': 'no_auth',
                                 })
        else:
            redirect(reverse('application:login'))
    return view2
