from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),

    # Setor CRUD URLs
    path("setores/", views.setor_list, name="setor_list"),
    path("setores/<int:setor_id>/", views.setor_detail, name="setor_detail"),
    path("setores/novo/", views.setor_create, name="setor_create"),
    path("setores/<int:setor_id>/editar/", views.setor_edit,
         name="setor_edit"),
    path("setores/<int:setor_id>/excluir/",
         views.setor_delete,
         name="setor_delete"),
]
