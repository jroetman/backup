# Generated by Django 2.1.2 on 2018-12-08 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20181208_1925'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leveltype',
            name='type_id',
        ),
        migrations.RemoveField(
            model_name='leveltypelevels',
            name='type_id',
        ),
        migrations.AddField(
            model_name='leveltype',
            name='level_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.LevelType'),
        ),
    ]
