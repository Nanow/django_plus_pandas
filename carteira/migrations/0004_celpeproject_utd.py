# Generated by Django 3.0.1 on 2019-12-26 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carteira', '0003_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='celpeproject',
            name='utd',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='utd'),
        ),
    ]
