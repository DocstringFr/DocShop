# Generated by Django 3.2.9 on 2021-11-06 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20211106_1742'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('address_1', models.CharField(help_text='Adresse de voirie et numéro de rue.', max_length=1024)),
                ('address_2', models.CharField(help_text='Bâtiment, étage, lieu-dit...', max_length=1024)),
                ('city', models.CharField(max_length=1024)),
                ('zip_code', models.CharField(max_length=24)),
            ],
        ),
    ]