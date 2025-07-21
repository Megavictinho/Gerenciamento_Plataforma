from django.urls import path
from .views import *

urlpatterns = [
    path('cadastrar/', cadastrar_pessoa, name='cadastrar_pessoa'),
    path('', listar_pessoas, name='listar_pessoas'),
    path('logs/', listar_logs, name='listar_logs'),
    path('pessoa/<int:pessoa_id>/editar/', editar_pessoa, name='editar_pessoa'),
    path('pessoa/<int:pessoa_id>/excluir/', excluir_pessoa, name='excluir_pessoa'),
    path('dashboard/', index_dashboard, name='index_dashboard'),
    path('dashboardgeral/', dashboard, name='dashboard'),
    path('dashboard/plataforma/<int:plataforma_id>/', dashboard_plataforma, name='dashboard_plataforma'),
]