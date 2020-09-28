from django.db import models


class Tithely(models.Model):

    net_amount = models.FloatField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    giving_type = models.CharField(max_length=50)
    trans_date = models.DateField(auto_now=False)


    def __str__(self):
        return f'{self.first_name}-{self.last_name}'
    
