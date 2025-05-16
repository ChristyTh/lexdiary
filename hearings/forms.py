from django import forms
from .models import Hearing

class HearingForm(forms.ModelForm):
    class Meta:
        model = Hearing
        fields = ['hearing_date', 'stage', 'notes']
        widgets = {
            'hearing_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'stage': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
