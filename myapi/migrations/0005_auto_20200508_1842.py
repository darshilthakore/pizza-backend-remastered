# Generated by Django 2.0.12 on 2020-05-08 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0004_cartitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='cartitems', to='myapi.Cart'),
        ),
    ]
