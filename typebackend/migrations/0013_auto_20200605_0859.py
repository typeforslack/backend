# Generated by Django 3.0.5 on 2020-06-05 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('typebackend', '0012_auto_20200507_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paragraph',
            name='para',
            field=models.TextField(unique=True, verbose_name='Paragraph'),
        ),
    ]
