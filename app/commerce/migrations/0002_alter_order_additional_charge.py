# Generated by Django 4.2.7 on 2024-04-07 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='additional_charge',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='дополнительная плата'),
        ),
    ]
