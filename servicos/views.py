from django.shortcuts import render
from django.http import HttpRequest

# Create your views here.


def novo_servico(request: HttpRequest):
    return render(request, "novo_servico.html")
