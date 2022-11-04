from django.shortcuts import render
from django.http import HttpRequest
from .forms import FormServico

# Create your views here.


def novo_servico(request: HttpRequest):
    form = FormServico()

    return render(request, "novo_servico.html", {"form": form})
