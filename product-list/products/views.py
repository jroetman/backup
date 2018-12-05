from django.shortcuts import render

# Create your views here.
import datetime
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

#def update_field_colors(request, pk):
#    """View function for update color scale."""
#    field = get_object_or_404(Field, pk=pk)
#
#    # If this is a POST request then process the Form data
#    if request.method == 'POST':
#
#        # Create a form instance and populate it with data from the request (binding):
#        color_scale_form= ColorScaleForm(request.POST)
#
#        # Check if the form is valid:
#        if color_scale_form.is_valid():
#            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
#            field.palette = color_scale_form.palette['palette']
#            field.save()
#
#            # redirect to a new URL:
#            return HttpResponseRedirect(reverse('all-borrowed') )
#
#    context = {
#        'form': color_scale_form,
#        'field': field,
#    }
#
#    return render(request, 'models/color_scale.html', context)
#
