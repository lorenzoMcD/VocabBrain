from django import template
from django.contrib.auth.models import Group
import random

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter(name='has_def')
def has_def(definiton, word_id):
    wordid = Word.objects.get(id=word_id)
    mydef = wordid.definiton
    return mydef == definiton

@register.filter(name = 'shuffle')
def shuffle(arg):
    tmp = list(arg)[:]
    random.shuffle(tmp)
    return tmp


@register.filter
def index(indexable, i): 
	return indexable[i] 