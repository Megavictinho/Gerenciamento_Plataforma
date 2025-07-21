from django import forms
from .models import Pessoa, Plataforma, Log
from django.core.exceptions import ValidationError
from datetime import date

class PessoaForm(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = ['nome', 'cpf', 'data_entrada', 'data_saida', 'foto']

    def clean(self):
        cleaned_data = super().clean()
        entrada = cleaned_data.get('data_entrada')
        saida = cleaned_data.get('data_saida')

        if entrada and saida and entrada > saida:
            raise ValidationError("Data de entrada não pode ser maior que data de saída.")