from django.shortcuts import render, redirect
from .forms import PessoaForm
from .models import *
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.db.models import Q
from datetime import date

def cadastrar_pessoa(request):
    plataformas = Plataforma.objects.all()

    if request.method == 'POST':
        form = PessoaForm(request.POST, request.FILES)
        plataforma_id = request.POST.get('plataforma')

        if form.is_valid():
            pessoa = form.save(commit=False)
            entrada = pessoa.data_entrada
            saida = pessoa.data_saida
            conflito = Log.objects.filter(
                pessoa__cpf=pessoa.cpf,
                data_saida__gte=entrada,
                data_entrada__lte=saida,
            ).exists()
            if conflito:
                messages.error(request, "Essa pessoa já está alocada em outra plataforma nesse período.")
            else:
                pessoa.save()
                if plataforma_id:
                    plataforma = Plataforma.objects.get(id=plataforma_id)
                    Log.objects.create(
                        pessoa=pessoa,
                        plataforma=plataforma,
                        data_entrada=entrada,
                        data_saida=saida
                    )
                messages.success(request, "Pessoa cadastrada e alocada com sucesso!")
                return redirect('cadastrar_pessoa')
    else:
        form = PessoaForm()

    return render(request, 'core/cadastrar_pessoa.html', {'form': form, 'plataformas': plataformas})


def listar_pessoas(request):
    pessoas = Pessoa.objects.all().order_by('nome')
    logs_qs = Log.objects.select_related('plataforma', 'pessoa').order_by('-data_entrada')
    logs = {}
    for log in logs_qs:
        if log.pessoa_id not in logs:
            logs[log.pessoa_id] = log
    return render(request, 'core/listar_pessoas.html', {
        'pessoas': pessoas,
        'logs': logs,
    })


def listar_logs(request):
    logs = Log.objects.select_related('pessoa', 'plataforma').order_by('-data_entrada')
    return render(request, 'core/listar_logs.html', {'logs': logs})


def editar_pessoa(request, pessoa_id):
    pessoa = get_object_or_404(Pessoa, id=pessoa_id)
    log = Log.objects.filter(pessoa=pessoa).last()
    plataformas = Plataforma.objects.all()

    if request.method == 'POST':
        form = PessoaForm(request.POST, request.FILES, instance=pessoa)
        plataforma_id = request.POST.get('plataforma')

        if form.is_valid():
            nova_pessoa = form.save(commit=False)

            # Verifica conflitos de alocação com outras plataformas
            conflito = Log.objects.exclude(id=log.id if log else None).filter(
                pessoa__cpf=nova_pessoa.cpf,
                data_saida__gte=nova_pessoa.data_entrada,
                data_entrada__lte=nova_pessoa.data_saida,
            ).exists()

            if conflito:
                messages.error(request, "Essa pessoa já está alocada em outra plataforma nesse período.")
            else:
                nova_pessoa.save()
                if plataforma_id:
                    plataforma = Plataforma.objects.get(id=plataforma_id)
                    if log:
                        log.plataforma = plataforma
                        log.data_entrada = nova_pessoa.data_entrada
                        log.data_saida = nova_pessoa.data_saida
                        log.save()
                    else:
                        Log.objects.create(
                            pessoa=nova_pessoa,
                            plataforma=plataforma,
                            data_entrada=nova_pessoa.data_entrada,
                            data_saida=nova_pessoa.data_saida
                        )
                messages.success(request, "Pessoa atualizada com sucesso!")
                return redirect('listar_pessoas')

    else:
        form = PessoaForm(instance=pessoa)

    return render(request, 'core/editar_pessoa.html', {
        'form': form,
        'plataformas': plataformas,
        'plataforma_atual': log.plataforma.id if log else None
    })


def excluir_pessoa(request, pessoa_id):
    pessoa = get_object_or_404(Pessoa, id=pessoa_id)
    
    if request.method == 'POST':
        pessoa.delete()
        messages.success(request, "Pessoa removida com sucesso.")
        return redirect('listar_pessoas')

    return render(request, 'core/confirmar_exclusao.html', {'pessoa': pessoa})


def dashboard(request):
    hoje = now().date()
    plataformas = Plataforma.objects.all()

    plataformas_com_pessoas = []

    for plataforma in plataformas:
        logs_ativos = Log.objects.filter(
            plataforma=plataforma,
            data_entrada__lte=hoje,
        ).filter(
            Q(data_saida__gte=hoje) | Q(data_saida__isnull=True)
        ).select_related('pessoa')

        plataformas_com_pessoas.append({
            'plataforma': plataforma,
            'logs_ativos': logs_ativos,
        })

    return render(request, 'core/dashboard.html', {
        'plataformas_com_pessoas': plataformas_com_pessoas,
        'today': hoje,
    })


def dashboard_plataforma(request, plataforma_id):
    plataforma = get_object_or_404(Plataforma, id=plataforma_id)
    logs_ativos = Log.objects.filter(plataforma=plataforma, data_saida__gte=date.today())

    context = {
        'plataforma': plataforma,
        'logs_ativos': logs_ativos,
    }
    return render(request, 'core/dashboard_plataforma.html', context)


def index_dashboard(request):
    plataformas = Plataforma.objects.all()
    return render(request, 'core/index_dashboard.html', {'plataformas': plataformas})