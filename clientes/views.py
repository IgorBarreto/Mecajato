import re
import json
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.core import serializers
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
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
    carros = Carro.objects.filter(cliente=cliente[0])
    carros_json = json.loads(serializers.serialize("json", carros))
    carros_json = [
        {"fields": carro["fields"], "id": carro["pk"]} for carro in carros_json
    ]
    cliente_id = json.loads(serializers.serialize("json", cliente))[0]["pk"]
    data = {
        "cliente": clietes_json,
        "carros": carros_json,
        "client_id": cliente_id,
    }
    return JsonResponse(data)


@csrf_exempt
def update_carro(request: HttpRequest, id):
    nome_carro = request.POST.get("carro")
    placa_carro = request.POST.get("placa")
    ano_carro = request.POST.get("ano")
    carro = Carro.objects.get(id=id)
    lista_carros = Carro.objects.filter(placa=placa_carro).exclude(id=id)
    if lista_carros.exists():
        HttpResponse("Placa já existente")

    carro.carro = nome_carro
    carro.placa = placa_carro
    carro.ano = ano_carro
    carro.save()
    return HttpResponse("Daados alterados com sucesso")


def excluir_carro(request: HttpRequest, id):
    try:
        carro = Carro.objects.get(id=id)
        carro.delete()
        return redirect(
            reverse("clientes" + f"?aba=att_cliente&id_cliente={id}")
        )
    except:
        # TODO: EXIBIR MENSAGEM DE ERRO
        return redirect(reverse("clientes"))


def update_cliente(request: HttpRequest, id):
    body = json.loads(request.body)

    nome = body["nome"]
    sobrenome = body["sobrenome"]
    email = body["email"]
    cpf = body["cpf"]

    cliente = get_object_or_404(Cliente, id=id)
    try:
        cliente.nome = nome
        cliente.sobrenome = sobrenome
        cliente.email = email
        cliente.cpf = cpf
        cliente.save()
        return JsonResponse(
            {
                "status": "200",
                "nome": nome,
                "sobrenome": sobrenome,
                "email": email,
                "cpf": cpf,
            }
        )
    except:
        return JsonResponse({"status": "500"})
