# Generated by Django 5.0.2 on 2024-03-05 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property_manager', '0007_propertyfile_remove_property_documents_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertyfile',
            name='file',
            field=models.FileField(upload_to='property_documents/'),
        ),
    ]