from django.db import models
from datetime import date
from django.urls import reverse
from django.db.models import Sum
from phone_field import PhoneField

class RegistrationModel(models.Model):

    """This model is used to register church members to the database table 'RegistrationModel'"""
    first_name = models.CharField(max_length=250, blank=False)
    last_name = models.CharField(max_length=250, blank=False)
    middle_name = models.CharField(max_length=250, blank=True)
    date_of_birth = models.DateField(null=False, blank=False)
    street_address = models.CharField(max_length=250, blank=False)
    postal_code = models.CharField(max_length=20, blank=False)
    province = models.CharField(max_length=20, blank=False)
    country = models.CharField(max_length=20, blank=False)
    phone = PhoneField(blank=True, E164_only=False)
    email = models.EmailField(max_length=30, blank=True)

    class Meta:
        ordering = ('first_name', 'last_name',)

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'

    


class GivingModel(models.Model):

    # This model is used to record monies collected during service to the database table 'GivingModel'
    members = models.ForeignKey(RegistrationModel, on_delete=models.DO_NOTHING, related_name='members')
    giving_date = models.DateField(default=date.today, blank=False)
    offering_amount = models.FloatField(null=True, blank=True)
    tithe_amount = models.FloatField(null=True, blank=True)
    building_fund_amount = models.FloatField(null=True, blank=True)
    Other_amount = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ('-giving_date',)

    def __str__(self):
        return (f'Giving Date: {self.giving_date}, Offering Amount: {self.offering_amount},\
        Tithe Amount: {self.tithe_amount}, Building: {self.building_fund_amount}, Other: {self.Other_amount}\n')

