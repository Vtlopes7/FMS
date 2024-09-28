from django.shortcuts import render, redirect
from django.http import HttpResponse
from processos.models import Recepcao  # Importe a model Processo


def home(request):
    # Pega o valor do filtro da empresa se ele for enviado no GET
    empresa_filtro = request.GET.get('empresa', '')

    # Se a empresa foi informada, filtra por empresa, caso contrário, retorna todos
    if empresa_filtro:
        processos = Recepcao.objects.filter(empresa__icontains=empresa_filtro)
    else:
        processos = Recepcao.objects.all()

    return render(request, 'home.html', {'processos': processos, 'empresa_filtro': empresa_filtro})




def Recepção(request):
    return render(request, 'Recepção.html')
