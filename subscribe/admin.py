#coding:utf-8
from django.contrib import admin
from models import *


class InscricoesAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'data_inscricao', 'minicurso')
    list_filter = ('participacao', 'situacao', 'minicurso')



admin.site.register(Inscricoes, InscricoesAdmin)
admin.site.register(MiniCursos)
