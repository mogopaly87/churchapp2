from django.forms import ModelForm
from .models import JournalEntry

class EntryForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['form-0-entry_type'].widget.attrs.update({'class':'form-control'})
        self.fields['form-0-entry_value'].widget.attrs.update({'class':'form-control'})
        self.fields['form-0-entry_date'].widget.attrs.update({'class':'form-control'})
        self.fields['form-0-short_note'].widget.attrs.update({'class':'form-control'})
        
    class Meta:
        model = JournalEntry
        fields = '__all__'
        
