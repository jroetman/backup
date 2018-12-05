# Generated by Django 2.1.2 on 2018-11-07 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ColorScale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of this color scale', max_length=200)),
                ('domains', models.CharField(help_text='List of domains', max_length=200)),
                ('palette', models.CharField(help_text='List of colors matching domains', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('varname', models.CharField(help_text='Variable name as found in netcdf file', max_length=300)),
                ('alias', models.CharField(blank=True, help_text='Alias for this field', max_length=200)),
                ('units', models.CharField(blank=True, help_text='Units', max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(help_text='Level', max_length=20)),
                ('display_name', models.CharField(blank=True, help_text='name', max_length=10, null=True)),
                ('color_scale', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.ColorScale')),
            ],
        ),
        migrations.CreateModel(
            name='LevelType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_id', models.FloatField(help_text='Type Id')),
                ('name', models.CharField(blank=True, help_text='name', max_length=100, null=True)),
                ('description', models.CharField(blank=True, help_text='Units', max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name', max_length=200)),
                ('alias', models.CharField(blank=True, help_text='Name', max_length=200)),
                ('fieldtype', models.CharField(blank=True, help_text='Model type aod..', max_length=200)),
                ('path', models.CharField(help_text='Path for NETCDF file', max_length=200)),
                ('isdaily', models.BooleanField(help_text='Is this daily vs hourly data?')),
                ('time_format', models.CharField(default='"%Y%m%d_%H%M"', help_text='How is the timem formatted?', max_length=200)),
                ('time_regex', models.CharField(default='".*?_(\\d+_\\d+)_.*"', help_text='How to extract time from filename', max_length=200)),
                ('foot', models.CharField(blank=True, help_text='Footer for plots', max_length=200)),
                ('fields', models.ManyToManyField(blank=True, to='products.Field')),
            ],
        ),
        migrations.AddField(
            model_name='level',
            name='level_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.LevelType'),
        ),
        migrations.AddField(
            model_name='field',
            name='levels',
            field=models.ManyToManyField(blank=True, to='products.Level'),
        ),
        migrations.AddField(
            model_name='field',
            name='model',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.Product'),
        ),
    ]
