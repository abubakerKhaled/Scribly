# Generated by Django 5.1.2 on 2024-10-24 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=250, unique=True, unique_for_date='publish'),
        ),
    ]
