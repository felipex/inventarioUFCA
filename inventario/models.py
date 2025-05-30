from django.db import models


class MaterialOrigem(models.Model):
  tombo = models.CharField(max_length=10, null=False, unique=True)
  descricao = models.CharField(max_length=255)
  date_inc = models.DateField(auto_now_add=True)
  date_mod = models.DateField(auto_now=True)


class Setor(models.Model):
  codigo = models.CharField(
      max_length=10,  #
      null=False,  #
      unique=True)
  descricao = models.CharField(r'Descrição', max_length=255)
  date_inc = models.DateField(auto_now_add=True)
  date_mod = models.DateField(auto_now=True)


class Localizacao(models.Model):
  codigo = models.CharField(max_length=10, null=False, unique=True)
  descricao = models.CharField(max_length=255)
  setor = models.ForeignKey(Setor, on_delete=models.PROTECT)
  date_inc = models.DateField(auto_now_add=True)
  date_mod = models.DateField(auto_now=True)


class Material(models.Model):
  tombo = models.OneToOneField(MaterialOrigem,
                               blank=True,
                               null=True,
                               on_delete=models.PROTECT)
  descricao = models.CharField(max_length=255, blank=False)
  localizacao = models.ForeignKey(Localizacao, on_delete=models.PROTECT)
  date_inc = models.DateField(auto_now_add=True)
  date_mod = models.DateField(auto_now=True)
