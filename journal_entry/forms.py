from django.forms import ModelForm
from .models import JournalEntry

class EntryForm(ModelForm):

    class Meta:
        model = JournalEntry
        fields = '__all__'
        
