from django.contrib import admin
from .models import Plataforma, Pessoa, Log

@admin.register(Plataforma)
class PlataformaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)

@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'cpf', 'data_entrada', 'data_saida')
    search_fields = ('nome', 'cpf')
    list_filter = ('data_entrada', 'data_saida')

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('id', 'pessoa', 'plataforma', 'data_entrada', 'data_saida', 'duracao')
    search_fields = ('pessoa__nome', 'plataforma__nome')
    list_filter = ('data_entrada', 'data_saida')