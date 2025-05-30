from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import MaterialOrigem, Setor, Localizacao, Material


@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    # Lista de campos a serem exibidos na página de listagem
    list_display = ['codigo', 'descricao', 'total_localizacoes', 'date_inc', 'date_mod']
    
    # Campos que podem ser usados para busca
    search_fields = ['codigo', 'descricao']
    
    # Filtros laterais
    list_filter = ['date_inc', 'date_mod']
    
    # Campos somente leitura
    readonly_fields = ['date_inc', 'date_mod']
    
    # Organização dos campos no formulário
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('codigo', 'descricao')
        }),
        ('Timestamps', {
            'fields': ('date_inc', 'date_mod'),
            'classes': ('collapse',)
        }),
    )
    
    # Paginação
    list_per_page = 20
    
    # Ordenação padrão
    ordering = ['codigo']
    
    def total_localizacoes(self, obj):
        """Exibe o total de localizações relacionadas a este setor"""
        count = obj.localizacao_set.count()
        if count > 0:
            url = reverse('admin:inventario_localizacao_changelist') + f'?setor__id__exact={obj.id}'
            return format_html('<a href="{}">{} localização(ões)</a>', url, count)
        return '0 localizações'
    total_localizacoes.short_description = 'Localizações'
    
    def get_queryset(self, request):
        """Otimiza a query para incluir contagem de localizações"""
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('localizacao_set')


@admin.register(Localizacao)
class LocalizacaoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descricao', 'setor', 'total_materiais', 'date_inc']
    search_fields = ['codigo', 'descricao', 'setor__codigo', 'setor__descricao']
    list_filter = ['setor', 'date_inc']
    readonly_fields = ['date_inc', 'date_mod']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('codigo', 'descricao', 'setor')
        }),
        ('Timestamps', {
            'fields': ('date_inc', 'date_mod'),
            'classes': ('collapse',)
        }),
    )
    
    def total_materiais(self, obj):
        """Exibe o total de materiais nesta localização"""
        count = obj.material_set.count()
        if count > 0:
            url = reverse('admin:inventario_material_changelist') + f'?localizacao__id__exact={obj.id}'
            return format_html('<a href="{}">{} material(is)</a>', url, count)
        return '0 materiais'
    total_materiais.short_description = 'Materiais'


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['tombo_info', 'descricao', 'localizacao', 'setor_info', 'date_inc']
    search_fields = ['descricao', 'tombo__tombo', 'localizacao__codigo', 'localizacao__setor__codigo']
    list_filter = ['localizacao__setor', 'localizacao', 'date_inc']
    readonly_fields = ['date_inc', 'date_mod']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('tombo', 'descricao', 'localizacao')
        }),
        ('Timestamps', {
            'fields': ('date_inc', 'date_mod'),
            'classes': ('collapse',)
        }),
    )
    
    def tombo_info(self, obj):
        """Exibe informação do tombo se existir"""
        if obj.tombo:
            return obj.tombo.tombo
        return 'Sem tombo'
    tombo_info.short_description = 'Tombo'
    
    def setor_info(self, obj):
        """Exibe o setor através da localização"""
        return obj.localizacao.setor.codigo if obj.localizacao and obj.localizacao.setor else 'Sem setor'
    setor_info.short_description = 'Setor'


@admin.register(MaterialOrigem)
class MaterialOrigemAdmin(admin.ModelAdmin):
    list_display = ['tombo', 'descricao', 'tem_material_associado', 'date_inc']
    search_fields = ['tombo', 'descricao']
    list_filter = ['date_inc']
    readonly_fields = ['date_inc', 'date_mod']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('tombo', 'descricao')
        }),
        ('Timestamps', {
            'fields': ('date_inc', 'date_mod'),
            'classes': ('collapse',)
        }),
    )
    
    def tem_material_associado(self, obj):
        """Verifica se o tombo tem material associado"""
        try:
            if obj.material:
                url = reverse('admin:inventario_material_change', args=[obj.material.id])
                return format_html('<a href="{}">Sim - Ver material</a>', url)
        except:
            pass
        return 'Não'
    tem_material_associado.short_description = 'Material Associado'


# Customização do site admin
admin.site.site_header = 'Sistema de Inventário'
admin.site.site_title = 'Inventário Admin'
admin.site.index_title = 'Painel de Administração'
