import django_filters

from .models import *
from django.contrib.auth.models import User


class OrderFilter(django_filters.FilterSet):
    class Meta:

        model = User
        fields = ['username', 'email']
