

from django import template

register = template.Library()
from application.models import *


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def is_shared(update):
    return isinstance(update,ProfileSharesStatus)

@register.filter
def is_pic(update):
    return isinstance(update,Photos)




@register.filter
def get_name(update):
    instance = Status.objects.get(update_id=update.update_id)
    if(instance.page_email is None):
        profile = RegularProfile.objects.get(email=instance.regular_profile_email.email)
        name = profile.firstname+" "+profile.lastname
        return name
    
    else:
        page = Page.objects.get(email=instance.page_email.email)
        name = page.title
        return name

@register.filter
def get_sharer(update):
    mail = update.regular_profile_email.email
    profile = RegularProfile.objects.get(email=mail)
    return profile.firstname+" "+profile.lastname



@register.filter
def apply(job):
    app = AppliesFor.objects.filter(job=job)
    people = []
    for each in app:
        person = RegularProfile.objects.get(email=each.regular_profile_email.email)
        people.append(person)
    return people
