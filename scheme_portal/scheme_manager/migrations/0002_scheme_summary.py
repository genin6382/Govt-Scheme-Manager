# Generated by Django 3.2.25 on 2024-07-20 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheme_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheme',
            name='summary',
            field=models.TextField(default=''),
        ),
    ]
