import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

#class ColorScaleForm(forms.Form):
#    palette = forms.CharField(max_length=200,help_text="A comma seperated list of hex vals")
#
#    def clean_palette(self):
#        data = self.cleaned_data['palette']
#        
#        # Check if a date is not in the past. 
#        dataparts = data.split(",")
#
#        for p in dataparts:
#            match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', p) 
#            if not match:
#                raise ValidationError(_('Invalid value: ' + p))
#
#        # Remember to always return the cleaned data.
#        return data
