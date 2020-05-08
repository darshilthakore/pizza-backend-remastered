# Generated by Django 2.0.12 on 2020-05-08 22:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0005_auto_20200508_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cartuser', to=settings.AUTH_USER_MODEL),
        ),
    ]
