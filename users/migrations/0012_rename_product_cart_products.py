# Generated by Django 4.2.4 on 2023-11-11 00:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_cart_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='product',
            new_name='products',
        ),
    ]
