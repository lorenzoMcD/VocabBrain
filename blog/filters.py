import django_filters

from .models import *
from django.contrib.auth.models import User

# this is class for the filters on pages suchs as teacherlookup


class OrderFilter(django_filters.FilterSet):
    class Meta:

        model = User

        # here you can add other fields to filter by that
        # are based on the User model
        fields = ['username']
