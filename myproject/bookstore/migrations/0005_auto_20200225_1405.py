# Generated by Django 3.0.1 on 2020-02-25 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0004_book_publishday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='publishDay',
            field=models.DateField(null=True),
        ),
    ]
