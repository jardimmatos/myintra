from django import forms
from .models import Atendimento

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Atendimento
        fields = ('avaliacao',)