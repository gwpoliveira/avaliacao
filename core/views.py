import datetime
import matplotlib
matplotlib.use('Agg')  # Configura o backend "Agg" para evitar problemas com GUI em ambiente de servidor
import matplotlib.pyplot as plt
import base64
import io  # Importa o módulo io
from io import BytesIO  # Importa BytesIO para uso em funções
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from .models import SetorAvaliado, AulaAvaliada
from .forms import SetorForm, AulaForm
from django.contrib.auth.decorators import login_required


def home(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')  # Redireciona para o Painel se o usuário estiver logado
    return render(request, 'home.html')  # Exibe a página inicial para visitantes

@login_required()
def admin_dashboard(request):
    ano_atual = datetime.datetime.now().year

    # Coleta as avaliações de setor e aula para o ano atual
    avaliacoes_setor = SetorAvaliado.objects.filter(data_avaliacao__year=ano_atual)
    avaliacoes_aula = AulaAvaliada.objects.filter(data_avaliacao__year=ano_atual)

    # Contagem das avaliações por setor
    setores = dict(SetorAvaliado.SETORES_CHOICES)
    avaliacao_por_setor = {setor: {'Ótimo': 0, 'Regular': 0, 'Ruim': 0} for setor in setores.values()}

    for avaliacao in avaliacoes_setor:
        setor_nome = setores.get(avaliacao.setor)
        if avaliacao.avaliacao == 'otimo':
            avaliacao_por_setor[setor_nome]['Ótimo'] += 1
        elif avaliacao.avaliacao == 'regular':
            avaliacao_por_setor[setor_nome]['Regular'] += 1
        elif avaliacao.avaliacao == 'ruim':
            avaliacao_por_setor[setor_nome]['Ruim'] += 1

    # Gerar gráfico de setor
    grafico_base64_setor = gerar_grafico(avaliacao_por_setor, 'Avaliações de Setor')

    # Contagem das avaliações por aula (para gerar o gráfico)
    avaliacao_tipos_aula = {'Ótimo': 0, 'Regular': 0, 'Ruim': 0}
    for avaliacao in avaliacoes_aula:
        if avaliacao.avaliacao == 'otimo':
            avaliacao_tipos_aula['Ótimo'] += 1
        elif avaliacao.avaliacao == 'regular':
            avaliacao_tipos_aula['Regular'] += 1
        elif avaliacao.avaliacao == 'ruim':
            avaliacao_tipos_aula['Ruim'] += 1

    # Gerar gráfico de aula
    grafico_base64_aula = gerar_grafico(avaliacao_tipos_aula, 'Avaliações de Aula')

    context = {
        'ano_atual': ano_atual,
        'avaliacao_por_setor': avaliacao_por_setor,
        'avaliacoes_aula': avaliacoes_aula,
        'grafico_base64_setor': grafico_base64_setor,
        'grafico_base64_aula': grafico_base64_aula,
    }
    return render(request, 'admin_dashboard.html', context)

def avaliar_setor(request):
    if request.method == 'POST':
        form = SetorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('agradecimento')
    else:
        form = SetorForm()
    return render(request, 'avaliar_setor.html', {'form': form})

def avaliar_aula(request):
    if request.method == 'POST':
        form = AulaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('agradecimento')
    else:
        form = AulaForm()
    return render(request, 'avaliar_aula.html', {'form': form})


def gerar_grafico(data, titulo):
    plt.figure(figsize=(6, 4))

    if isinstance(list(data.values())[0], dict):  # Verifica se é um dicionário aninhado
        # Para gráficos de setores
        tipos = list(next(iter(data.values())).keys())  # ['Ótimo', 'Regular', 'Ruim']
        cores = ['green', 'orange', 'red']

        for i, tipo in enumerate(tipos):
            valores = [setor_data[tipo] for setor_data in data.values()]
            plt.bar(data.keys(), valores, label=tipo, color=cores[i])
    else:
        # Para gráficos simples, como o de aula
        plt.bar(data.keys(), data.values(), color=['green', 'orange', 'red'])

    plt.title(titulo)
    plt.xlabel('Categorias')
    plt.ylabel('Quantidade')
    plt.legend(loc="upper right")

    # Salva o gráfico em um buffer para conversão em base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    grafico_base64 = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    return grafico_base64


def grafico_avaliacao_setor(request):
    ano_atual = datetime.datetime.now().year
    setores = dict(SetorAvaliado.SETORES_CHOICES)  # Mapeia as opções de setor para exibição no template
    avaliacao_por_setor = {setor: {'Ótimo': 0, 'Regular': 0, 'Ruim': 0} for setor in setores.values()}

    # Filtra as avaliações de setor para o ano atual e conta cada tipo de avaliação
    avaliacoes_setor = SetorAvaliado.objects.filter(data_avaliacao__year=ano_atual)
    for avaliacao in avaliacoes_setor:
        setor_nome = setores.get(avaliacao.setor, 'Outro')
        if avaliacao.avaliacao == 'otimo':
            avaliacao_por_setor[setor_nome]['Ótimo'] += 1
        elif avaliacao.avaliacao == 'regular':
            avaliacao_por_setor[setor_nome]['Regular'] += 1
        elif avaliacao.avaliacao == 'ruim':
            avaliacao_por_setor[setor_nome]['Ruim'] += 1

    # Gera o gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    setores_nomes = list(setores.values())
    avaliacao_cores = ['green', 'orange', 'red']

    for i, tipo in enumerate(['Ótimo', 'Regular', 'Ruim']):
        valores = [avaliacao_por_setor[setor][tipo] for setor in setores_nomes]
        ax.bar(setores_nomes, valores, label=tipo, color=avaliacao_cores[i])

    ax.set_title(f'Avaliações de Setor em {ano_atual}')
    ax.set_xlabel('Setores')
    ax.set_ylabel('Quantidade')
    ax.legend()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    grafico_base64 = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    context = {
        'grafico_base64': grafico_base64,
        'avaliacao_por_setor': avaliacao_por_setor,
        'ano_atual': ano_atual
    }

    return render(request, 'relatorio_setor.html', context)


def grafico_avaliacao_aula(request):
    ano_atual = datetime.datetime.now().year
    avaliacoes_aula = AulaAvaliada.objects.filter(data_avaliacao__year=ano_atual)

    avaliacao_tipos = {'Ótimo': 0, 'Regular': 0, 'Ruim': 0}
    for avaliacao in avaliacoes_aula:
        if avaliacao.avaliacao == 'otimo':
            avaliacao_tipos['Ótimo'] += 1
        elif avaliacao.avaliacao == 'regular':
            avaliacao_tipos['Regular'] += 1
        elif avaliacao.avaliacao == 'ruim':
            avaliacao_tipos['Ruim'] += 1

    grafico_base64 = gerar_grafico(avaliacao_tipos, f'Avaliações de Aula em {ano_atual}')

    context = {
        'grafico_base64': grafico_base64,
        'avaliacao_tipos': avaliacao_tipos,
        'ano_atual': ano_atual
    }

    return render(request, 'relatorio_aula.html', context)

def grafico_avaliacoes(request):
    ano_atual = datetime.datetime.now().year
    avaliacoes_setor = SetorAvaliado.objects.filter(data_avaliacao__year=ano_atual)
    avaliacoes_aula = AulaAvaliada.objects.filter(data_avaliacao__year=ano_atual)

    avaliacao_tipos = {'Ótimo': 0, 'Regular': 0, 'Ruim': 0}
    for avaliacao in avaliacoes_setor:
        if avaliacao.avaliacao == 'otimo':
            avaliacao_tipos['Ótimo'] += 1
        elif avaliacao.avaliacao == 'regular':
            avaliacao_tipos['Regular'] += 1
        elif avaliacao.avaliacao == 'ruim':
            avaliacao_tipos['Ruim'] += 1
    for avaliacao in avaliacoes_aula:
        if avaliacao.avaliacao == 'otimo':
            avaliacao_tipos['Ótimo'] += 1
        elif avaliacao.avaliacao == 'regular':
            avaliacao_tipos['Regular'] += 1
        elif avaliacao.avaliacao == 'ruim':
            avaliacao_tipos['Ruim'] += 1

    grafico_base64 = gerar_grafico(avaliacao_tipos, f'Avaliações Combinadas em {ano_atual}')

    context = {
        'grafico_base64': grafico_base64,
        'avaliacao_tipos': avaliacao_tipos,
        'ano_atual': ano_atual
    }

    return render(request, 'admin_dashboard.html', context)

def agradecimento(request):
    return render(request, 'agradecimento.html')

def exportar_excel(request):
    ano_atual = datetime.datetime.now().year
    avaliacoes_setor = SetorAvaliado.objects.filter(data_avaliacao__year=ano_atual)

    # Organiza os dados em um DataFrame para o Excel
    data = []
    for avaliacao in avaliacoes_setor:
        data.append({
            'Setor': dict(SetorAvaliado.SETORES_CHOICES).get(avaliacao.setor),
            'Avaliação': dict(SetorAvaliado._meta.get_field('avaliacao').choices).get(avaliacao.avaliacao),
            'Data de Avaliação': avaliacao.data_avaliacao.strftime('%Y-%m-%d %H:%M')
        })
    df = pd.DataFrame(data)

    # Configura a resposta para baixar o arquivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=Avaliacoes_Setor_{ano_atual}.xlsx'
    df.to_excel(response, index=False, engine='openpyxl')
    return response

def exportar_pdf(request):
    ano_atual = datetime.datetime.now().year
    avaliacoes_setor = SetorAvaliado.objects.filter(data_avaliacao__year=ano_atual)

    # Cria o buffer e o canvas para gerar o PDF
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setTitle(f"Avaliações de Setor {ano_atual}")

    # Adiciona título
    p.drawString(100, 800, f"Relatório de Avaliações de Setor ({ano_atual})")

    # Posiciona as colunas no PDF
    y_position = 750
    p.drawString(80, y_position, "Setor")
    p.drawString(180, y_position, "Avaliação")
    p.drawString(300, y_position, "Data de Avaliação")
    y_position -= 20

    # Adiciona os dados das avaliações
    for avaliacao in avaliacoes_setor:
        p.drawString(80, y_position, dict(SetorAvaliado.SETORES_CHOICES).get(avaliacao.setor))
        p.drawString(180, y_position, dict(SetorAvaliado._meta.get_field('avaliacao').choices).get(avaliacao.avaliacao))
        p.drawString(300, y_position, avaliacao.data_avaliacao.strftime('%Y-%m-%d %H:%M'))
        y_position -= 20
        if y_position < 50:  # Quebra de página se necessário
            p.showPage()
            y_position = 800

    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"Avaliacoes_Setor_{ano_atual}.pdf")

def exportar_excel_aula(request):
    ano_atual = datetime.datetime.now().year
    avaliacoes_aula = AulaAvaliada.objects.filter(data_avaliacao__year=ano_atual)

    # Organiza os dados em um DataFrame para o Excel
    data = []
    for avaliacao in avaliacoes_aula:
        data.append({
            'Matrícula': avaliacao.matricula,
            'Nome': avaliacao.nome,
            'WhatsApp': avaliacao.whatsapp,
            'Aula': avaliacao.aula,
            'Avaliação': dict(AulaAvaliada._meta.get_field('avaliacao').choices).get(avaliacao.avaliacao),
            'Data de Avaliação': avaliacao.data_avaliacao.strftime('%Y-%m-%d %H:%M')
        })
    df = pd.DataFrame(data)

    # Configura a resposta para baixar o arquivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=Avaliacoes_Aula_{ano_atual}.xlsx'
    df.to_excel(response, index=False, engine='openpyxl')
    return response

def exportar_pdf_aula(request):
    ano_atual = datetime.datetime.now().year
    avaliacoes_aula = AulaAvaliada.objects.filter(data_avaliacao__year=ano_atual)

    # Cria o buffer e o canvas para gerar o PDF
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setTitle(f"Avaliações de Aula {ano_atual}")

    # Adiciona título
    p.drawString(100, 800, f"Relatório de Avaliações de Aula ({ano_atual})")

    # Posiciona as colunas no PDF
    y_position = 750
    p.drawString(40, y_position, "Matrícula")
    p.drawString(120, y_position, "Nome")
    p.drawString(220, y_position, "Aula")
    p.drawString(320, y_position, "Avaliação")
    p.drawString(420, y_position, "Data de Avaliação")
    y_position -= 20

    # Adiciona os dados das avaliações
    for avaliacao in avaliacoes_aula:
        p.drawString(40, y_position, avaliacao.matricula)
        p.drawString(120, y_position, avaliacao.nome)
        p.drawString(220, y_position, avaliacao.aula)
        p.drawString(320, y_position, dict(AulaAvaliada._meta.get_field('avaliacao').choices).get(avaliacao.avaliacao))
        p.drawString(420, y_position, avaliacao.data_avaliacao.strftime('%Y-%m-%d %H:%M'))
        y_position -= 20
        if y_position < 50:  # Quebra de página se necessário
            p.showPage()
            y_position = 800

    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"Avaliacoes_Aula_{ano_atual}.pdf")


