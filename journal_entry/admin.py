from django.contrib import admin
from .models import JournalEntry

@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('entry_date','entry_type', 'entry_value', 'short_note')
    list_filter = ('entry_date','entry_type',)
