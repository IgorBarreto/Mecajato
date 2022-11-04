from django.contrib import admin

# Register your models here.
from .models import CategoriaManutencao, Servico

admin.site.register(CategoriaManutencao)
admin.site.register(Servico)
