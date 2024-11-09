from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView  # Importar LoginView e LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  # Redireciona para login após o logout
    path('grafico-avaliacao-setor/', views.grafico_avaliacao_setor, name='grafico_avaliacao_setor'),
    path('grafico-avaliacao-aula/', views.grafico_avaliacao_aula, name='grafico_avaliacao_aula'),
    path('grafico-avaliacoes/', views.grafico_avaliacoes, name='grafico_avaliacoes'),
    path('avaliar-setor/', views.avaliar_setor, name='avaliar_setor'),
    path('avaliar-aula/', views.avaliar_aula, name='avaliar_aula'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('exportar-excel/', views.exportar_excel, name='exportar_excel'),
    path('exportar-pdf/', views.exportar_pdf, name='exportar_pdf'),
    path('agradecimento/', views.agradecimento, name='agradecimento'),
    path('exportar-excel-aula/', views.exportar_excel_aula, name='exportar_excel_aula'),
    path('exportar-pdf-aula/', views.exportar_pdf_aula, name='exportar_pdf_aula'),
]
