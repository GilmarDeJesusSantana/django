from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from receitas_app.models import Receita
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    receitas = Receita.objects.order_by('-date_receita').filter(publicado=True)
    paginator = Paginator(receitas, 3)
    page = request.GET.get('page')
    receitas_por_pagina = paginator.get_page(page)
    dados = {
        'receitas': receitas_por_pagina
    }
    return render(request, 'receitas/index.html', dados)


def receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita_a_exibir = {'receita': receita}
    return render(request, 'receitas/receita.html', receita_a_exibir)


def cria_receita(request):
    if request.method == 'POST':
        nome_receita = request.POST['nome_receita']
        ingredientes = request.POST['ingredientes']
        modo_preparo = request.POST['modo_preparo']
        tempo_preparo = request.POST['tempo_preparo']
        rendimento = request.POST['rendimento']
        categoria = request.POST['categoria']
        foto_receita = request.FILES['foto_receita']
        user = get_object_or_404(User, pk=request.user.id)
        receita = Receita.objects.create(pessoa=user,
                                         nome_receita=nome_receita,
                                         ingredientes=ingredientes,
                                         modo_preparo=modo_preparo,
                                         tempo_preparo=tempo_preparo,
                                         rendimento=rendimento,
                                         categoria=categoria,
                                         foto_receita=foto_receita)
        receita.save()
        return redirect('dashboard')
    else:
        return render(request, 'receitas/cria_receita.html')


def edita_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita_a_editar = {'receita': receita}
    return render(request, 'receitas/edita_receita.html', receita_a_editar)


def deleta_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita.delete()
    return redirect('dashboard')


def atualiza_receita(request):
    if request.method == 'POST':
        receita_id = request.POST['receita_id']
        receita_em_edicao = Receita.objects.get(pk=receita_id)
        receita_em_edicao.nome_receita = request.POST['nome_receita']
        receita_em_edicao.ingredientes = request.POST['ingredientes']
        receita_em_edicao.modo_preparo = request.POST['modo_preparo']
        receita_em_edicao.tempo_preparo = request.POST['tempo_preparo']
        receita_em_edicao.rendimento = request.POST['rendimento']
        receita_em_edicao.categoria = request.POST['categoria']
        if 'foto_receita' in request.FILES:
            receita_em_edicao.foto_receita = request.FILES['foto_receita']
        receita_em_edicao.save()
        return redirect('dashboard')
