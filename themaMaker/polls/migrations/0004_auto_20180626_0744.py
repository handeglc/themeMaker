# Generated by Django 2.0.6 on 2018-06-26 07:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0003_color_color_groups_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='liked_color_groups',
        ),
        migrations.AddField(
            model_name='color_groups',
            name='how_many_colors',
            field=models.IntegerField(default=170),
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='user_profile',
            name='liked_color_groups',
            field=models.ManyToManyField(to='polls.Color_Groups'),
        ),
        migrations.AddField(
            model_name='user_profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
