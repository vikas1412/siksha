# Generated by Django 3.2.8 on 2021-11-13 06:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('create_exam', '0008_userinfo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='fullname',
        ),
    ]
