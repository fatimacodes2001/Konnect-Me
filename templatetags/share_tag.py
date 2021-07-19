from django import template
import re
register = template.Library()
from datetime import datetime

from application.models import *



@register.simple_tag
def get_share_instance(update):
    status = Status.objects.get(update_id=update.update_id)
    return status





@register.simple_tag
def get_pfp( email ):
    return "../media/"+email+"/"+email+"/"+email+".jpg"

@register.simple_tag
def get_pfp_mini( email ):
    return "../media/"+email+"/"+email+"/"+email+"35.jpg"

@register.simple_tag
def share_status( update_id = 0, email = ''):
    return ProfileSharesStatus.objects.filter(regular_profile_email = email , update_id = update_id).order_by('regular_profile_email') or ProfileSharesPhotos.objects.filter(regular_profile_email = email , update_id = update_id).order_by('regular_profile_email')

@register.simple_tag
def like_status( update_id = 0, email = ''):
    return (ProfileLikesStatus.objects.filter(regular_profile_email = email , update_id = update_id).order_by('regular_profile_email') or ProfileLikesPhotos.objects.filter(regular_profile_email = email , update_id = update_id).order_by('regular_profile_email'))

@register.simple_tag
def get_mail(update):
    print(update)
    if(update.page_email is None):
        return update.regular_profile_email.email
    else:
        return update.page_email.email
    



@register.simple_tag
def page_like_status( update_id = 0, email = ''):
    return PageLikesStatus.objects.filter(page_email = email , update_id = update_id).order_by('page_email') or PageLikesPhotos.objects.filter(page_email = email , update_id = update_id).order_by('page_email')

@register.simple_tag
def like_check( update_id = 0, email = ''):
    return (PageLikesStatus.objects.filter(page_email = email , update_id = update_id).order_by('page_email')
    or PageLikesPhotos.objects.filter(page_email = email , update_id = update_id).order_by('page_email')
    or ProfileLikesStatus.objects.filter(regular_profile_email = email , update_id = update_id).order_by('regular_profile_email')
    or ProfileLikesPhotos.objects.filter(regular_profile_email = email , update_id = update_id).order_by('regular_profile_email'))


@register.simple_tag
def is_profile( object ):
    return (isinstance(object,RegularProfile) or isinstance(object,ProfileFollowsProfile)
    or isinstance(object,ProfileLikesStatus) or isinstance(object,PageFollowsPage)
    or isinstance(object,ProfileLikesPhotos))

@register.simple_tag
def is_page( object ):
    return (isinstance(object,Page) or isinstance(object,PageFollowsProfile)
    or isinstance(object,ProfileFollowsPage) or isinstance(object,PageLikesStatus)
    or isinstance(object,PageLikesPhotos))

@register.simple_tag
def is_self( email1 , email2 ):
    return email1 == email2

@register.simple_tag
def is_pfp( album_id ):
    return Album.objects.filter(album_id = album_id,name = "Profile Pictures")


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


def getDuration(then, now = datetime.now(), interval = "default"):

    # Returns a duration as specified by variable interval
    # Functions, except totalDuration, returns [quotient, remainder]

    duration = now - then # For build-in functions
    duration_in_s = duration.total_seconds()

    def years():
      return divmod(duration_in_s, 31536000) # Seconds in a year=31536000.

    def days(seconds = None):
      return divmod(seconds if seconds != None else duration_in_s, 86400) # Seconds in a day = 86400

    def hours(seconds = None):
      return divmod(seconds if seconds != None else duration_in_s, 3600) # Seconds in an hour = 3600

    def minutes(seconds = None):
      return divmod(seconds if seconds != None else duration_in_s, 60) # Seconds in a minute = 60

    def seconds(seconds = None):
      if seconds != None:
        return divmod(seconds, 1)
      return duration_in_s

    def totalDuration():
        y = years()
        d = days(y[1]) # Use remainder to calculate next variable
        h = hours(d[1])
        m = minutes(h[1])
        s = seconds(m[1])

        return int(seconds())
    return {

        'years': int(years()[0]),
        'days': int(days()[0]),
        'hours': int(hours()[0]),
        'minutes': int(minutes()[0]),
        'seconds': int(seconds()),
        'default': totalDuration()

    }[interval]


@register.simple_tag
def get_time( datetime ):

    # Example usage
    then = datetime.replace(tzinfo=None)
    now = datetime.now()

    time = getDuration(then)
    time_tag = " seconds ago"

    if time == 1:
        time_tag = " second ago"
        time = getDuration(then)

    if time > 60:
        time = getDuration(then, now, 'seconds')

        if time>1:
            time_tag = " seconds ago"
        else:
            time_tag = " second ago"

        if time > 60:
            time = getDuration(then, now, 'minutes')

            if time>1:
                time_tag = " minutes ago"
            else:
                time_tag = " minute ago"

            if time > 60:
                time = getDuration(then, now, 'hours')
                if time>1:
                    time_tag = " hours ago"
                else:
                    time_tag = " hour ago"

                if time > 24:
                    time = getDuration(then, now, 'days')
                    if time>1:
                        time_tag = " days ago"
                    else:
                        time_tag = " day ago"

                    if time > 365:
                        time = getDuration(then, now, 'years')
                        if time>1:
                            time_tag = " years ago"
                        else:
                            time_tag = " year ago"



    if time < 1:
        date = "just now"
    else:
        date = str(time)+time_tag

    return date
