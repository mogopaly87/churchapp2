from django.db import models
from datetime import date


class JournalEntry(models.Model):
    ENTRY_CHOICES = [
        ('Hospitality Exp', 'Hospitality Exp'),
        ('Pastor\'s gift', 'Pastor\'s gift'),
        ('Welfare Exp','Welfare Exp'),
        ('Other', 'Other'),
    ]

    entry_type = models.CharField(choices=ENTRY_CHOICES, max_length=200)
    entry_value = models.FloatField(blank=False, null=False)
    entry_date =models.DateField(default=date.today, blank=False, null=False)
    short_note = models.TextField(max_length=300, blank=False, null=False, default='')

    class Meta:
        verbose_name_plural = "Journal Entries"

    def __str__(self):
        return self.entry_type
