# Generated by Django 5.2 on 2025-04-18 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document_type',
            field=models.CharField(choices=[('evaluacion', 'Evaluacion'), ('material', 'Material'), ('reporte', 'Reporte')], max_length=15),
        ),
    ]
