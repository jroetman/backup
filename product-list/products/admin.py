from django.contrib import admin
from .models import Product, ColorScale, Field, Level, LevelType

# Register your models here.

admin.site.register(ColorScale)
admin.site.register(LevelType)

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
   list_display = ('level', 'display_name', 'level_type', 'color_scale')

@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
   list_display = ('model', 'varname', 'alias', 'units')
   fieldsets= [(None, {'fields': ('model', 'varname', 'alias', 'units', 'levels')})]
    

#class ColorInline(admin.TabularInline):
#   model = Field
    
#class CategoryForm(ModelForm):
#    class Meta:
#        model = ColorScale 
#        fields = '__all__'
#
#@admin.register(ColorScale)
#class ColorScaleAdmin(admin.ModelAdmin):
#    form = CategoryForm
#


