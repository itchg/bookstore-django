# Generated by Django 3.0.1 on 2019-12-25 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moment',
            name='content',
            field=models.CharField(max_length=300),
        ),
    ]
