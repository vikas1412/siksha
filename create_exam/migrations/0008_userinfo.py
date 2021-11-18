# Generated by Django 3.2.8 on 2021-11-09 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('create_exam', '0007_todo'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=200)),
                ('password', models.CharField(max_length=40)),
            ],
        ),
    ]