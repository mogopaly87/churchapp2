from .models import RegistrationModel
from django import forms


class RegForm(forms.ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control reg-form'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control reg-form'})
        self.fields['middle_name'].widget.attrs.update({'class': 'form-control reg-form'})
        self.fields['date_of_birth'].widget.attrs.update({'class': 'form-control reg-form', 
                                                            'pattern': '[0-9]{4}-[0-9]{2}-[0-9]{2}',
                                                            'placeholder': 'yyyy-mm-dd', 'type':'date'})
                                                            
        self.fields['street_address'].widget.attrs.update({'class': 'form-control reg-form'})
        self.fields['postal_code'].widget.attrs.update({'class': 'form-control reg-form', 
                                                        'pattern': '[A-Za-z]{1}[0-9]{1}[A-Za-z]{1} [0-9]{1}[A-Za-z]{1}[0-9]{1}', 
                                                        'placeholder': 'A1A 2B2'})
        self.fields['province'].widget.attrs.update({'class': 'form-control reg-form', 
                                                    'pattern':'[A-Za-z]{2}', 
                                                    'placeholder': 'AB, BC, NL'})
        self.fields['country'].widget.attrs.update({'class': 'form-control reg-form'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control reg-form', 
                                                    'pattern': '[0-9]{3}-[0-9]{3}-[0-9]{4}', 
                                                    'placeholder': '000-000-0000'})
        self.fields['email'].widget.attrs.update({'class': 'form-control reg-form',
                                                    'type': 'email'})
    class Meta:
        model = RegistrationModel
        exclude = ['slug']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type':'date'})
        }

