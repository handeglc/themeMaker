# Generated by Django 2.0.6 on 2018-07-02 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20180629_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_profile',
            name='liked_color_groups',
            field=models.ManyToManyField(blank=True, to='polls.Color_Groups'),
        ),
    ]