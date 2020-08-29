from .models import GivingModel
import django_filters

class GivingFilter(django_filters.FilterSet):
    class Meta:
        model = GivingModel
        fields = {
            'giving_date':['gt', 'lt'],
        }