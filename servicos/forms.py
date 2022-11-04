from django.forms import ModelForm

from .models import Servico, CategoriaManutencao


class FormServico(ModelForm):
    class Meta:
        model = Servico
        """
        maneira de criar o form
        """
        # fields = [
        #     "titulo",
        #     "cliente",
        #     "categoria_manutencao",
        #     "data_inicio",
        #     "protocolo",
        # ]
        exclude = ["finalzado", "protocolo"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["titulo"].widget.attrs.update({"class": "form-control "})

        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control "})
            self.fields[field].widget.attrs.update(
                {"placeholder": str(field).title()}
            )
            choices = list()
            for i, j in self.fields["categoria_manutencao"].choices:
                categoria = CategoriaManutencao.objects.get(titulo=j)
                print(categoria.get_titulo_display())
