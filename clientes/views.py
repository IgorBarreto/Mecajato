import re
import json
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.core import serializers
from .models import Cliente, Carro

# Create your views here.
def clientes(request: HttpRequest):
    if request.method == "GET":
        clienteslist = Cliente.objects.all()
        return render(request, "clientes.html", {"clientes": clienteslist})
    elif request.method == "POST":
        nome = request.POST.get("nome")
        sobrenome = request.POST.get("sobrenome")
        email = request.POST.get("email")
        cpf = request.POST.get("cpf")
        carros = request.POST.getlist("carro")
        placas = request.POST.getlist("placa")
        anos = request.POST.getlist("ano")
        print(nome, sobrenome, email, cpf)
        cliente = Cliente.objects.filter(cpf=cpf)
        if cliente.exists():
            return render(
                request,
                "clientes.html",
                {
                    "nome": nome,
                    "sobrenome": sobrenome,
                    "email": email,
                    "carros": zip(carros, placas, anos),
                },
            )

        if not re.fullmatch(
            re.compile(
                r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
            ),
            email,
        ):
            # TODO: Adicionar mensagens
            return render(
                request,
                "clientes.html",
                {
                    "nome": nome,
                    "sobrenome": sobrenome,
                    "cpf": cpf,
                    "carros": zip(carros, placas, anos),
                },
            )
        cliente = Cliente(
            nome=nome,
            sobrenome=sobrenome,
            email=email,
            cpf=cpf,
        )
        cliente.save()
        for carros, placa, ano in zip(carros, placas, anos):
            carro = Carro(
                carro=carros,
                placa=placa,
                ano=ano,
                cliente=cliente,
            )
            carro.save()
        return HttpResponse("teste")


def att_cliente(request: HttpRequest):
    id_cliente = request.POST.get("id_cliente")
    cliente = Cliente.objects.filter(id=id_cliente)
    clietes_json = json.loads(serializers.serialize("json", cliente))[0][
        "fields"
    ]
    return JsonResponse(clietes_json)
