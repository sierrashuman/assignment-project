# Generated by Django 3.2.7 on 2021-11-15 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_id',
            field=models.IntegerField(default=15929, unique=True),
            preserve_default=False,
        ),
    ]
