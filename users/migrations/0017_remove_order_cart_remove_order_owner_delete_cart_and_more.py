# Generated by Django 4.2.4 on 2023-11-15 04:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_remove_order_address_remove_order_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='order',
            name='owner',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
