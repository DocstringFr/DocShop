# Generated by Django 3.2.9 on 2021-11-06 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopper',
            name='email',
            field=models.EmailField(max_length=240, unique=True),
        ),
    ]