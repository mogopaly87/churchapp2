from django.contrib import admin
from .models import Tithely


@admin.register(Tithely)
class TithelyAdmin(admin.ModelAdmin):
    list_display = ('trans_date', 'first_name', 'last_name', 'net_amount', 'giving_type')
