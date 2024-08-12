# Generated by Django 4.2.4 on 2024-08-07 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0014_remove_order_cart_orderitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='ordered',
        ),
        migrations.AddField(
            model_name='cart',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='created_at'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='created_at'),
        ),
        migrations.AddField(
            model_name='order',
            name='time_of_order',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='created_at'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='created_at'),
        ),
    ]
