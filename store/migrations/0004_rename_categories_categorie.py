# Generated by Django 4.0.2 on 2022-03-13 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_product_category'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Categories',
            new_name='Categorie',
        ),
    ]