# Generated by Django 4.0.2 on 2022-03-27 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_remove_cart_orders_cart_ordered_cart_product_and_more'),
        ('store', '0006_categorie_slug_product_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='ordered',
            new_name='finished',
        ),
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
        migrations.RemoveField(
            model_name='order',
            name='quantity',
        ),
        migrations.AddField(
            model_name='order',
            name='cart',
            field=models.ManyToManyField(to='account.Cart'),
        ),
        migrations.AddField(
            model_name='order',
            name='finished_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
