from django.contrib import admin
from .models import RegistrationModel, GivingModel

# Register your models here.

@admin.register(GivingModel)
class GivingModelAdmin(admin.ModelAdmin):
    list_display = ('members', 'giving_date','offering_amount', 'tithe_amount', 'building_fund_amount','Other_amount')
    list_filter = ('giving_date',)

@admin.register(RegistrationModel)
class RegisterationModelAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'phone', 'street_address', 'id')
    search_fields = ('first_name', 'last_name')