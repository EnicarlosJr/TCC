from django.shortcuts import render

def tela_inicial(request):
    return render(request, 'tela_inicial.html')
