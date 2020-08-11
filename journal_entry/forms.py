from django.forms import ModelForm
from .models import JournalEntry

class EntryForm(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['entry_type'].widget.attrs.update({'class':'form-control'})
        self.fields['entry_value'].widget.attrs.update({'class':'form-control'})
        self.fields['entry_date'].widget.attrs.update({'class':'form-control',
                                                            'pattern': '[0-9]{4}-[0-9]{2}-[0-9]{2}',
                                                            'placeholder': 'yyyy-mm-dd'})
        self.fields['short_note'].widget.attrs.update({'class':'form-control'})
        
    class Meta:
        model = JournalEntry
        fields = '__all__'
        
