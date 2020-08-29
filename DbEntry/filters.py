from .models import GivingModel
import django_filters
from django import forms

class GivingFilter(django_filters.FilterSet):
    class Meta:
        model = GivingModel
        fields = {
            'giving_date':['gt', 'lt'],
        }