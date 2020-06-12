import django_filters

from .models import *
from django.contrib.auth.models import User

# this is class for the filters on pages such as teacherlookup


class OrderFilter(django_filters.FilterSet):
    class Meta:

        model = User

        # here you can add other fields to filter by that
        # are based on the User model
        fields = ['username', 'first_name', 'last_name', ]


# filter for student progess tracker page
class ProgressFilter(django_filters.FilterSet):
    class Meta:

        model = Testtaker

        # here you can add other fields to filter by that
        # are based on the Testtaker model
        fields = ['test']
