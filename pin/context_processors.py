from django.core.cache import cache
from django.contrib.auth.models import User
from pin.forms import PinForm
from pin.models import Category


def pin_form(request):
    return {'pin_form': PinForm}


def pin_categories(request):
    cats = Category.objects.all()

    return {'cats': cats}


def is_super_user(request):
    
    if request.user.is_superuser:
        return {'is_super_user': True}

    return {'is_super_user': False}


def user__id(request):
    return {'user__id': request.user.id}
