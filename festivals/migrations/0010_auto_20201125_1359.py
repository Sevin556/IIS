# Generated by Django 3.1.3 on 2020-11-25 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('festivals', '0009_auto_20201124_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='t_stage',
            name='popis',
            field=models.TextField(blank=True),
        ),
    ]