# Generated by Django 2.0.6 on 2018-06-20 07:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file',
            old_name='upload',
            new_name='file_field',
        ),
        migrations.RenameField(
            model_name='file',
            old_name='name',
            new_name='name_field',
        ),
    ]
