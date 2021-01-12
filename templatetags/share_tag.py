from django import template

register = template.Library()

from application.models import ProfileSharesStatus,ProfileLikesStatus,ProfileFollowsProfile,PageFollowsProfile,ProfileFollowsPage,ProfileLikesStatus,PageLikesStatus

@register.simple_tag
def share_status( update_id = 0, email = ''):
    return ProfileSharesStatus.objects.filter(regular_profile_email = email , update_id = update_id).order_by('regular_profile_email')

@register.simple_tag
def like_status( update_id = 0, email = ''):
    return ProfileLikesStatus.objects.filter(regular_profile_email = email , update_id = update_id).order_by('regular_profile_email')

@register.simple_tag
def is_profile( object ):
    return isinstance(object,ProfileFollowsProfile) or isinstance(object,ProfileLikesStatus)

@register.simple_tag
def is_page( object ):
    return isinstance(object,PageFollowsProfile) or isinstance(object,ProfileFollowsPage) or isinstance(object,PageLikesStatus)
