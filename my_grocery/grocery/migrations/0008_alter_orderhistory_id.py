# Generated by Django 5.1.1 on 2024-09-25 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grocery', '0007_remove_orderproduct_price_remove_orderproduct_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderhistory',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
