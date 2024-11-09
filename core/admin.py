from django.contrib import admin
from .models import SetorAvaliado, AulaAvaliada

@admin.register(SetorAvaliado)
class SetorAvaliadoAdmin(admin.ModelAdmin):
    list_display = ('setor', 'avaliacao', 'data_avaliacao')
    list_filter = ('avaliacao', 'data_avaliacao')
    date_hierarchy = 'data_avaliacao'

@admin.register(AulaAvaliada)
class AulaAvaliadaAdmin(admin.ModelAdmin):
    list_display = ('aula', 'avaliacao', 'data_avaliacao')
    list_filter = ('avaliacao', 'data_avaliacao')
    date_hierarchy = 'data_avaliacao'
