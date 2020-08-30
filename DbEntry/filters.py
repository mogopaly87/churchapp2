from .models import GivingModel
import django_filters
from django import forms

class GivingFilter(django_filters.FilterSet):

    # To change the default label names, override the __init__ method
    # ... of 'FilterSet' using the __init__ method below
    # Source: https://github.com/carltongibson/django-filter/issues/107

    def __init__(self, *args, **kwargs):
        super(GivingFilter, self).__init__(*args, **kwargs)
        self.filters['giving_date__gt'].label = 'Start Date'
        self.filters['giving_date__lt'].label = 'End Date'

    class Meta:
        model = GivingModel
        fields = {
            'giving_date':['gt', 'lt'],
        }