# Generated by Django 5.0.2 on 2024-03-04 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tanant', '0007_tanant_broker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tanant',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
