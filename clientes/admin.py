from django.contrib import admin

# Register your models here.
from .models import Cliente, Carro

admin.site.register(Cliente)
admin.site.register(Carro)
