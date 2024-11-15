# Generated by Django 5.1.3 on 2024-11-10 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_aulaavaliada_curso_alter_aulaavaliada_avaliacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aulaavaliada',
            name='curso',
            field=models.CharField(choices=[('administracao', 'Administração'), ('ciencias_contabeis', 'Ciências Contábeis'), ('direito', 'Direito'), ('educacao_fisica', 'Educação Física'), ('enfermagem', 'Enfermagem'), ('fisioterapia', 'Fisioterapia'), ('fonoaudiologia', 'Fonoaudiologia'), ('pedagogia', 'Pedagogia'), ('psicologia', 'Psicologia'), ('servico_social', 'Serviço Social'), ('sistemas_informacao', 'Sistemas de Informação')], default='administracao', max_length=250),
        ),
    ]
