# from django import template
#
# from ..models import Staff
#
# register = template.Library()
#
#
# def user_post(request):
#     get_user = Staff.objects.filter(user=request.user).first()
#     return get_user
from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        return False

    return group in user.groups.all()


