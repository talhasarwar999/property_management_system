# Generated by Django 5.0.2 on 2024-03-04 15:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('broker', '0001_initial'),
        ('tanant', '0006_alter_tanant_agreement_document_alter_tanant_images_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tanant',
            name='broker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='broker_tenant_user', to='broker.broker'),
        ),
    ]
