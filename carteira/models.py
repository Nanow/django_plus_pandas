from django.db import models
import pandas as pd


class Task(models.Model):
    """ Model responsavel pelas atividades em um projeto """
    service_number = models.CharField(max_length=500, blank=False, null=False, verbose_name='Número do serviço')
    name = models.CharField(max_length=1500, null=False, blank=False, verbose_name='Texto breve')
    description = models.TextField(null=False, blank=False, verbose_name='Texto longo', help_text='Texto longo')
    measurement_unit = models.CharField(verbose_name='Unidade de medida', max_length=500, null=False, blank=False)
    merchandise_group = models.CharField(max_length=255, null=False, blank=False, help_text='Grupo de Mercadoria',
                                         verbose_name='Grupo de Mercadoria')
    valuation_class = models.CharField(verbose_name='classe da avaliação', max_length=500, null=False, blank=False)
    tax_rate_code = models.CharField(verbose_name='Código tarifa fiscal', max_length=500, null=False, blank=False)
    service_nature = models.CharField(verbose_name='Natureza do serviço', max_length=500, null=False, blank=False)
    gm_description = models.CharField(max_length=500, null=False, blank=False)
    value = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tasks'
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['name']


class CelpeProject(models.Model):
    """ Projeto para a celpe """
    project_code = models.CharField(max_length=250, unique=True, blank=False, null=False,
                                    verbose_name='Código do projeto')
    is_priority = models.BooleanField(default=False, null=False, verbose_name='Prioritário')
    city = models.CharField(max_length=500, null=False, blank=False, verbose_name='cidade')
    invoice_code = models.BigIntegerField(null=True, blank=True, verbose_name='Número da nota fiscal')
    qtd_posts = models.IntegerField(default=0, null=False, blank=False, verbose_name='Quantidade de postes')
    km_dead_wire = models.FloatField(null=True, blank=True, default=0, verbose_name='Quilometragem de linha morta')
    km_live_wire = models.FloatField(null=True, blank=True, default=0, verbose_name='Quilometragem de linha viva')
    start_date = models.DateTimeField(null=False, blank=False, verbose_name='Data de incio')
    finish_date = models.DateTimeField(null=True, blank=True, verbose_name='Data de termino')
    deadline_date = models.DateTimeField(null=True, blank=True, verbose_name='Data prevista')
    instalation_number = models.BigIntegerField(null=True, blank=True, verbose_name='data de instalação')
    invoice_generated = models.BigIntegerField(null=True, blank=True, verbose_name='Nota fiscal gerada')
    barrament_code = models.BigIntegerField(null=True, blank=True, verbose_name='Número do barramento')
    is_service_order = models.BooleanField(default=False, null=False, blank=False, verbose_name='Ordem de Serviço')

    class Meta:
        db_table = 'celpe_projects'
        verbose_name = 'Projeto da Celpe'
        verbose_name_plural = 'Projetos da Celpe'
        ordering = ['id']


class Carteira(models.Model):
    """  Carteira """
    file = models.FileField()
    data = models.DateTimeField()

    def __str__(self):
        return self.file.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Carteira, self).save()
        data = pd.read_excel(self.file.path, sheet_name='CÓD. CS')
        print(data.columns.ravel())
