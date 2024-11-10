from django import forms
from .models import SetorAvaliado, AulaAvaliada


class SetorForm(forms.ModelForm):
    class Meta:
        model = SetorAvaliado
        fields = ['nome', 'whatsapp', 'setor', 'avaliacao']

    def __init__(self, *args, **kwargs):
        super(SetorForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs[
                'class'] = 'form-control'  # Aplica a classe 'form-control' do Bootstrap a todos os campos

class AulaForm(forms.ModelForm):
    class Meta:
        model = AulaAvaliada
        fields = ['matricula', 'nome', 'whatsapp', 'curso', 'aula', 'avaliacao']  # Inclui o campo curso
# class AulaForm(forms.ModelForm):
#     class Meta:
#         model = AulaAvaliada
#         fields = ['matricula', 'nome', 'whatsapp', 'aula', 'avaliacao']
#
#     def __init__(self, *args, **kwargs):
#         super(AulaForm, self).__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs['class'] = 'form-control'
