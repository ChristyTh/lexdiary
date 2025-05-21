from django import forms
from .models import Stage

class StageForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = ['date', 'stage_name', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'stage_name': forms.TextInput(attrs={'class': 'form-control tagify-stage'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
