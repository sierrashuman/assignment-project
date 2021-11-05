# Generated by Django 3.2.7 on 2021-11-05 17:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment_app', '0007_merge_0005_auto_20211101_2030_0006_alter_pdf_pdf_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdf',
            name='pdf_file',
            field=models.FileField(upload_to='pdfs/', validators=[django.core.validators.FileExtensionValidator(['pdf'])]),
        ),
    ]
