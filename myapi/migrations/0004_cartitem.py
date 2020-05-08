# Generated by Django 2.0.12 on 2020-05-08 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0003_auto_20200508_1609'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('baseprice', models.FloatField(default=0)),
                ('extraprice', models.FloatField(default=0)),
                ('quantity', models.IntegerField(default=1)),
                ('total', models.FloatField(default=0)),
                ('cart', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='cartitem', to='myapi.Cart')),
                ('topping', models.ManyToManyField(blank=True, related_name='carttopping', to='myapi.Topping')),
            ],
        ),
    ]
