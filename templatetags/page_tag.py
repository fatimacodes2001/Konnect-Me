from django import template
import re
register = template.Library()

from application.models import *

@register.simple_tag
def share_status( update_id = 0, email = ''):
    return ProfileSharesStatus.objects.filter(regular_profile_email = email , update_id = update_id).order_by('regular_profile_email')

@register.simple_tag
def like_status( update_id = 0, email = ''):
    return ProfileLikesStatus.objects.filter(regular_profile_email = email , update_id = update_id).order_by('regular_profile_email')

@register.simple_tag
def is_profile( object ):
    return isinstance(object,RegularProfile) or isinstance(object,ProfileFollowsProfile) or isinstance(object,ProfileLikesStatus)

@register.simple_tag
def is_page( object ):
    return isinstance(object,Page) or isinstance(object,PageFollowsProfile) or isinstance(object,ProfileFollowsPage) or isinstance(object,PageLikesStatus)

@register.simple_tag
def is_self( email1 , email2 ):
    return email1 == email2



@register.simple_tag
def get_pfp_path ( email ):
    return "media/"+email+"/"+email+"/"+email+".jpg"

@register.simple_tag
def get_pfp_icon_path ( email ):
    return "media/"+email+"/"+email+"/"+email+"35.jpg"



@register.simple_tag
def get_follower_profile_id( email ):
    return "follower-profile-"+re.sub(r'[^\w]',"-",email)

@register.simple_tag
def get_follower_page_id( email ):
    return "follower-page-"+re.sub(r'[^\w]',"-",email)



@register.simple_tag
def get_un_follower_profile_id( email):
    return "un-follower-profile-"+re.sub(r'[^\w]',"-",email)

@register.simple_tag
def get_un_follower_page_id( email ):
    return "un-follower-page-"+re.sub(r'[^\w]',"-",email)



@register.simple_tag
def get_un_following_profile_id( email):
    return "un-following-profile-"+re.sub(r'[^\w]',"-",email)

@register.simple_tag
def get_un_following_page_id( email ):
    return "un-following-page-"+re.sub(r'[^\w]',"-",email)



@register.simple_tag
def get_following_profile_id( email):
    return "following-profile-"+re.sub(r'[^\w]',"-",email)

@register.simple_tag
def get_following_page_id( email ):
    return "following-page-"+re.sub(r'[^\w]',"-",email)



@register.simple_tag
def get_suggestion_profile_id( email):
    return "suggestion-profile-"+re.sub(r'[^\w]',"-",email)

@register.simple_tag
def get_suggestion_page_id( email ):
    return "suggestion-page-"+re.sub(r'[^\w]',"-",email)



@register.simple_tag
def get_liker_un_following_profile_id( email):
    return "liker-un-following-profile-"+re.sub(r'[^\w]',"-",email)

@register.simple_tag
def get_liker_un_following_page_id( email ):
    return "liker-un-following-page-"+re.sub(r'[^\w]',"-",email)

@register.simple_tag
def get_liker_following_profile_id( email):
    return "liker-following-profile-"+re.sub(r'[^\w]',"-",email)

@register.simple_tag
def get_liker_following_page_id( email ):
    return "liker-following-page-"+re.sub(r'[^\w]',"-",email)



@register.simple_tag
def get_sharer_un_following_profile_id( email):
    return "sharer-un-following-profile-"+re.sub(r'[^\w]',"-",email)

@register.simple_tag
def get_sharer_un_following_page_id( email ):
    return "sharer-un-following-page-"+re.sub(r'[^\w]',"-",email)

@register.simple_tag
def get_sharer_following_profile_id( email):
    return "sharer-following-profile-"+re.sub(r'[^\w]',"-",email)

@register.simple_tag
def get_sharer_following_page_id( email ):
    return "sharer-following-page-"+re.sub(r'[^\w]',"-",email)
