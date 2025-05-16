from django import forms
from .models import Case

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['case_number', 'case_name']
        widgets = {
            'case_number': forms.TextInput(attrs={'class': 'form-control'}),
            'case_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
