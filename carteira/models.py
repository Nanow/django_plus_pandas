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
    value = models.FloatField(null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tasks'
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['name']


class Tasks(models.Model):
    file = models.FileField()

    def __str__(self):
        return "atividades"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Tasks, self).save()
        xlsx = pd.ExcelFile(self.file.path)
        data = xlsx.parse(0)
        print(data.head(0))
        num_servico = data.count()['Numero do servico']
        for i in range(num_servico):
            row = data.iloc[i, :]
            service_number = row['Numero do servico']
            name = row['Texto breve']
            description = row['Texto longo']
            measurement_unit = row['Unidade de Medida']
            merchandise_group = row['Grupo de Mercadoria']
            valuation_class = row['Classe de avaliação']
            tax_rate_code = row['Código tarifa fiscal']
            service_nature = row['Natureza do Serviço']
            gm_description = row['Descrição do GM']
            value = row['Valor']
            Task.objects.create(service_number=service_number, name=name, description=description,
                                measurement_unit=measurement_unit, merchandise_group=merchandise_group,
                                valuation_class=valuation_class, tax_rate_code=tax_rate_code,
                                service_nature=service_nature, gm_description=gm_description, value=value)


class CelpeProject(models.Model):
    """ Projeto para a celpe """
    project_code = models.CharField(max_length=250, unique=True, blank=False, null=False,
                                    verbose_name='Código do projeto')
    is_priority = models.BooleanField(default=False, null=False, verbose_name='Prioritário')
    invoice_code = models.BigIntegerField(null=True, blank=True, verbose_name='Número da nota fiscal')
    city = models.CharField(max_length=500, null=False, blank=False, verbose_name='cidade')
    utd = models.CharField(max_length=500, null=True, blank=True, verbose_name='utd')
    qtd_posts = models.IntegerField(default=0, null=True, blank=True, verbose_name='Quantidade de postes')
    km_dead_wire = models.FloatField(null=True, blank=True, default=0, verbose_name='Quilometragem de linha morta')
    km_live_wire = models.FloatField(null=True, blank=True, default=0, verbose_name='Quilometragem de linha viva')
    start_date = models.DateTimeField(null=True, blank=True, verbose_name='Data de incio')
    finish_date = models.DateTimeField(null=True, blank=True, verbose_name='Data de termino')
    deadline_date = models.DateTimeField(null=True, blank=True, verbose_name='Data prevista')
    instalation_number = models.BigIntegerField(null=True, blank=True, verbose_name='data de instalação')
    invoice_generated = models.BigIntegerField(null=True, blank=True, verbose_name='Nota fiscal gerada')
    barrament_code = models.BigIntegerField(null=True, blank=True, verbose_name='Número do barramento')
    is_service_order = models.BooleanField(default=False, null=False, blank=False, verbose_name='Ordem de Serviço')

    def __str__(self):
        return self.project_code

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
        xlsx = pd.ExcelFile(self.file.path)
        data = xlsx.parse(0)
        projects_num = data.count()['Projeto']

        # try:
        #     print(data.head(0))
        #
        # except Exception as ex:
        #
        #     print("Deu algo errado {}".format(type(ex)))
        #
        # print("Número de projetos {}".format(projects_num))
        for i in range(projects_num):
            row = data.iloc[i, :]
            project_code = row['Projeto']
            is_priority = type(row['Prioridade']) is str
            invoice_code = row['Nota']
            main_scope = row['Escopo Principal']
            secondary_scope = row['Escopo Secundario']
            city = row['Local']
            utd = row['UTD']
            qtd_posts = row['Total de Postes']
            km_dead_wire = row['KM AT']
            km_dead_wire = row['KM BT']
            start_date = row['Inicio Prev da Obra']
            finish_date = row['Fim Prev da Obra']
            deadline_date = row['PRAZO FINAL']
            project, updated = CelpeProject.objects.update_or_create(project_code=project_code, is_priority=is_priority,
                                                                     invoice_code=invoice_code,
                                                                     city=city, utd=utd, qtd_posts=qtd_posts,
                                                                     km_dead_wire=km_dead_wire,
                                                                     km_live_wire=km_dead_wire, start_date=None,
                                                                     finish_date=None,
                                                                     deadline_date=None, instalation_number=None,
                                                                     invoice_generated=None,
                                                                     barrament_code=None, is_service_order=False)
            if not updated:
                print("Já existe")
