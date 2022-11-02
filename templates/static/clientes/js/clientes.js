function add_carro() {

    container = document.getElementById('form-carro')

    html = "<br>\
    <div class='row'>\
        <div class='col-md'>\
            <input type='text' placeholder='Carro' class='form-control' name='carro'/>\
        </div>\
        <div class='col-md'>\
            <input type='text' placeholder='Placa' class='form-control' name='placa'/>\
        </div>\
        <div class='col-md'>\
            <input type='number' placeholder='Ano' class='form-control' name='ano'/>\
        </div>\
    </div>"

    container.innerHTML += html
}

function exibir_form(tipo) {
    add_cliente = document.getElementById('adicionar-cliente');
    att_clientes = document.getElementById('att_clientes');

    if (tipo === "1") {
        att_clientes.style.display = 'none';
        add_cliente.style.display = 'block';
    }
    else if (tipo === "2") {
        add_cliente.style.display = 'none';
        att_clientes.style.display = 'block';
    }
}

function dados_cliente() {
    cliente = document.getElementById('cliente-select');
    console.log(cliente.value)
    csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value
    id_cliente = cliente.value
    data = new FormData()
    data.append('id_cliente', id_cliente)
    fetch("atualiza_cliente", {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrf_token
        },
        body: data
    }).then(function (result) {
        return result.json()
    }).then(function (data) {
        document.getElementById('form-att-cliente').style.display = 'block'

        nome = document.getElementById('nome')
        nome.value = data['nome']

        sobrenome = document.getElementById('sobrenome')
        sobrenome.value = data['sobrenome']

        cpf = document.getElementById('cpf')
        cpf.value = data['cpf']

        email = document.getElementById('email')
        email.value = data['email']
    })
}
