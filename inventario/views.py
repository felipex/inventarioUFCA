from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'inventario/index.html')
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Count
from .models import Setor, Localizacao, Material

def index(request):
    return render(request, 'inventario/index.html')

def setor_list(request):
    """Lista todos os setores com informações adicionais"""
    setores = Setor.objects.annotate(
        total_localizacoes=Count('localizacao')
    ).order_by('codigo')
    
    context = {
        'setores': setores,
        'total_setores': setores.count()
    }
    return render(request, 'inventario/setor_list.html', context)

def setor_detail(request, setor_id):
    """Exibe detalhes de um setor específico"""
    setor = get_object_or_404(Setor, id=setor_id)
    localizacoes = setor.localizacao_set.annotate(
        total_materiais=Count('material')
    ).order_by('codigo')
    
    context = {
        'setor': setor,
        'localizacoes': localizacoes,
        'total_localizacoes': localizacoes.count()
    }
    return render(request, 'inventario/setor_detail.html', context)

def setor_create(request):
    """Cria um novo setor"""
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        descricao = request.POST.get('descricao')
        
        if codigo and descricao:
            try:
                setor = Setor.objects.create(
                    codigo=codigo,
                    descricao=descricao
                )
                messages.success(request, f'Setor {codigo} criado com sucesso!')
                return redirect('setor_detail', setor_id=setor.id)
            except Exception as e:
                messages.error(request, f'Erro ao criar setor: {str(e)}')
        else:
            messages.error(request, 'Código e descrição são obrigatórios.')
    
    return render(request, 'inventario/setor_form.html', {'action': 'Criar'})

def setor_edit(request, setor_id):
    """Edita um setor existente"""
    setor = get_object_or_404(Setor, id=setor_id)
    
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        descricao = request.POST.get('descricao')
        
        if codigo and descricao:
            try:
                setor.codigo = codigo
                setor.descricao = descricao
                setor.save()
                messages.success(request, f'Setor {codigo} atualizado com sucesso!')
                return redirect('setor_detail', setor_id=setor.id)
            except Exception as e:
                messages.error(request, f'Erro ao atualizar setor: {str(e)}')
        else:
            messages.error(request, 'Código e descrição são obrigatórios.')
    
    context = {
        'setor': setor,
        'action': 'Editar'
    }
    return render(request, 'inventario/setor_form.html', context)

def setor_delete(request, setor_id):
    """Exclui um setor (com verificação de dependências)"""
    setor = get_object_or_404(Setor, id=setor_id)
    
    if request.method == 'POST':
        # Verifica se existem localizações associadas
        localizacoes_count = setor.localizacao_set.count()
        if localizacoes_count > 0:
            messages.error(request, f'Não é possível excluir o setor {setor.codigo}. Existem {localizacoes_count} localização(ões) associada(s).')
            return redirect('setor_detail', setor_id=setor.id)
        
        try:
            codigo = setor.codigo
            setor.delete()
            messages.success(request, f'Setor {codigo} excluído com sucesso!')
            return redirect('setor_list')
        except Exception as e:
            messages.error(request, f'Erro ao excluir setor: {str(e)}')
            return redirect('setor_detail', setor_id=setor.id)
    
    context = {
        'setor': setor,
        'localizacoes_count': setor.localizacao_set.count()
    }
    return render(request, 'inventario/setor_confirm_delete.html', context)
