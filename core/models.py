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
    CURSO_CHOICES = [
        ('administracao', 'Administração'),
        ('ciencias_contabeis', 'Ciências Contábeis'),
        ('direito', 'Direito'),
        ('educacao_fisica', 'Educação Física'),
        ('enfermagem', 'Enfermagem'),
        ('fisioterapia', 'Fisioterapia'),
        ('fonoaudiologia', 'Fonoaudiologia'),
        ('pedagogia', 'Pedagogia'),
        ('psicologia', 'Psicologia'),
        ('servico_social', 'Serviço Social'),
        ('sistemas_informacao', 'Sistemas de Informação'),
    ]

    matricula = models.CharField(max_length=20)
    nome = models.CharField(max_length=100)
    whatsapp = models.CharField(max_length=15)
    curso = models.CharField(max_length=250, choices=CURSO_CHOICES, default='administracao')  # Novo campo de curso
    aula = models.CharField(max_length=100)
    avaliacao = models.CharField(max_length=10, choices=[
        ('otimo', 'Ótimo'),
        ('regular', 'Regular'),
        ('ruim', 'Ruim')
    ])
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação {self.avaliacao} para {self.nome} no curso de {self.get_curso_display()}"
