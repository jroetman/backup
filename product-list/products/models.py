from django.db import models


class LevelType(models.Model):
    type_id   = models.FloatField(help_text='Type Id', blank=False, null=False)
    name      = models.CharField(max_length=100, help_text='name', blank=True, null=True)
    description = models.CharField(max_length=200, help_text='Units', blank=True, null=True)

    def __str__(self):
        """String for representing the Level Type"""
        return self.name

class Level(models.Model):
    level = models.CharField(help_text='Level', max_length=20, blank=False, null=False)
    display_name = models.CharField(max_length=10, help_text='name', blank=True, null=True)
    level_type= models.ForeignKey('LevelType', on_delete=models.SET_NULL, blank=True, null=True)
    color_scale = models.ForeignKey('ColorScale', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        """Level"""
        return   self.level_type.name + " " + str(self.level) + " " + str(self.color_scale)
# Create your models here.
class Field(models.Model):
    varname = models.CharField(max_length=300, help_text='Variable name as found in netcdf file')
    alias   = models.CharField(max_length=200, help_text='Alias for this field', blank=True)
    model   = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    units   = models.CharField(max_length=50, help_text='Units', blank=True, null=True)
    levels  = models.ManyToManyField(Level, blank=True)


    def __str__(self):
        """String for representing the Model object."""
        return self.varname


class ColorScale(models.Model):
    name        = models.CharField(max_length=200, help_text='Name of this color scale')
    domains     = models.CharField(max_length=200, help_text='List of domains')
    palette     = models.CharField(max_length=200, help_text='List of colors matching domains')

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Product(models.Model):
    name       = models.CharField(max_length=200, help_text='Name')
    alias      = models.CharField(max_length=200, help_text='Name', blank=True)
    fieldtype  = models.CharField(max_length=200, help_text='Model type aod..', blank=True)
    path       = models.CharField(max_length=200, help_text='Path for NETCDF file')
    isdaily    = models.BooleanField(help_text='Is this daily vs hourly data?')
    time_format = models.CharField(max_length=200,  default='"%Y%m%d_%H%M"', help_text='How is the timem formatted?')
    time_regex  = models.CharField(max_length=200,  default='".*?_(\d+_\d+)_.*"', help_text='How to extract time from filename')
    foot       = models.CharField(max_length=200, help_text='Footer for plots', blank=True)
    fields     = models.ManyToManyField(Field, blank=True)


    def __str__(self):
        """String for representing the Model object."""
        return self.name

