from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from django.views.generic import ListView

from datetime import datetime

from .models import Thing
from .forms import DateForm
  
def date_view(request): 
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            thing_date = form.cleaned_data['thing_date']
            year = thing_date.strftime("%Y")
            month = thing_date.strftime("%m")
            day = thing_date.strftime("%d")
            return redirect('five_fun_form', year=year, month=month, day=day)
 #            return redirect('product_detail', product_id=product_id)
    else:
        form = DateForm() 
    return render(request, 'date.html', {'form': form})

def five_fun_form(request, year, month, day):
    date_str = str(year) + "/" + str(month) + "/" + str(day)
    
    thing_date = datetime.strptime(date_str,'%Y/%m/%d')
    print(date_str, thing_date)

    ThingFormSet = modelformset_factory(Thing, 
                                        fields=('thing', 'photo'), 
                                        extra=3,
                                        min_num=1,
                                        )


    if request.method == 'POST':
        formset = ThingFormSet(request.POST, request.FILES)
        instances = formset.save(commit=False)        
        if formset.is_valid():
            for instance in instances:
                print(thing_date, dir(instance.photo), instance.thing_date, instance.thing)
                print(instance.photo)

                instance.thing_date = thing_date
                instance.funster = request.user 
                instance.save()
                print(instance.photo)
            print("j")
            return redirect('list')
        else:
            print(formset.errors)
 
    form = ThingFormSet(queryset=Thing.objects.filter(thing_date=thing_date))
    return render(request, 'index.html', {'form': form })


class ThingList(LoginRequiredMixin, ListView):
    model = Thing
