# Generated by Django 3.2.7 on 2021-10-28 03:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assignment_app', '0002_rename_courses_course'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='course',
            new_name='name',
        ),
    ]