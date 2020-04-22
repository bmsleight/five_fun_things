from django import forms 
from django.forms.widgets import SelectDateWidget
from django.utils import timezone

# creating a form  
class DateForm(forms.Form): 
    thing_date = forms.DateField(widget=SelectDateWidget(), initial=timezone.now)
