# Generated by Django 4.1.7 on 2023-04-08 07:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
        migrations.RemoveField(
            model_name='useraccount',
            name='profile_picture',
        ),
    ]
