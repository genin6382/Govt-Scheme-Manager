# Generated by Django 3.2.25 on 2024-07-26 03:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0002_alter_application_documents_submitted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='documents_submitted',
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='documents/')),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='applications.application')),
            ],
        ),
    ]
