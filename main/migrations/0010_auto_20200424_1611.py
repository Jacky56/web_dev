# Generated by Django 3.0.3 on 2020-04-24 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20200423_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='somecontext',
            name='synopsis',
            field=models.CharField(help_text='provide a synopsis for the content', max_length=200),
        ),
    ]