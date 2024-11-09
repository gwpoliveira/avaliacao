from django.db import models

class SetorAvaliado(models.Model):
    SETORES_CHOICES = [
        ('recepcao', 'Recepção'),
        ('financeiro', 'Financeiro'),
        ('academico', 'Acadêmico'),
        ('biblioteca', 'Biblioteca'),
        ('nti', 'NTI'),
    ]

    nome = models.CharField(max_length=100, blank=True, null=True)
    whatsapp = models.CharField(max_length=15, blank=True, null=True)
    setor = models.CharField(max_length=20, choices=SETORES_CHOICES)
    avaliacao = models.CharField(max_length=10, choices=[
        ('otimo', 'Ótimo'),
        ('regular', 'Regular'),
        ('ruim', 'Ruim')
    ])
    data_avaliacao = models.DateTimeField(auto_now_add=True)

class AulaAvaliada(models.Model):
    matricula = models.CharField(max_length=20)
    nome = models.CharField(max_length=100)
    whatsapp = models.CharField(max_length=15)
    aula = models.CharField(max_length=100)
    avaliacao = models.CharField(max_length=10, choices=[('😃', 'Ótimo'), ('😐', 'Regular'), ('☹️', 'Ruim')])
    data_avaliacao = models.DateTimeField(auto_now_add=True)  # Data e hora automática
