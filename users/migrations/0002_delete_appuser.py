# Generated by Django 4.2.4 on 2023-10-20 00:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AppUser',
        ),
    ]
