# Generated by Django 4.0.4 on 2022-06-08 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_statementfields'),
    ]

    operations = [
        migrations.AddField(
            model_name='statementfields',
            name='header',
            field=models.CharField(blank=True, choices=[('CA', 'Current assets:'), ('CL', 'Current liabilities:'), ('SE', "Stockholders' equity:")], max_length=1000, null=True, verbose_name='Header'),
        ),
    ]
