from django.contrib import admin

from .models import MaterialOrigem, Setor, Localizacao, Material

admin.site.register(MaterialOrigem)
admin.site.register(Setor)
admin.site.register(Localizacao)
admin.site.register(Material)
