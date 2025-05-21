from django import forms
from .models import Case

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['court', 'case_number', 'case_name', 'status']
        widgets = {
            'court': forms.TextInput(attrs={'class': 'tagify-input'}),
        }
