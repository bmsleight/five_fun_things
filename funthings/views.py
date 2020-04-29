from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory, Textarea, ClearableFileInput
from django.shortcuts import render, redirect
from django.views.generic import ListView

from django.http import HttpResponse

from datetime import datetime

from .models import Thing
from .forms import DateForm

# Word cloud
from wordcloud import WordCloud, ImageColorGenerator
import numpy as np
from PIL import Image
from tempfile import NamedTemporaryFile
from django.conf import settings



@login_required
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
                                        widgets={"thing": Textarea(attrs={'rows':2, 'cols':40, 'class': 'pure-form ', }),
                                                 "photo": ClearableFileInput(attrs={'class': 'custom-file-upload',}) }, 
                                        extra=4,
                                        min_num=1,
                                        max_num=6,
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
    return render(request, 'journal.html', {'form': form })

@login_required
def cloud_view(request): 
    things =  Thing.objects.filter(funster=request.user).values_list('thing', flat=True)
    all_thing_text = ""
    for r in things:
        all_thing_text = all_thing_text + " " + r
    colours = np.array(Image.open(settings.STATIC_ROOT + "/img/colours.png"))
    image_colors = ImageColorGenerator(colours)
    mask = np.array(Image.open(settings.STATIC_ROOT + "/img/mask.png"))
    wc = WordCloud(background_color="#FFDE3C", mask=mask)
    wc.generate(text=all_thing_text)
    wc.recolor(color_func=image_colors)
    tempFileObj = NamedTemporaryFile(mode='w+b',suffix='.png')
    wc.to_file(tempFileObj.name)
    with open(tempFileObj.name, 'rb') as f:
        image_data = f.read()
    return HttpResponse(image_data, content_type="image/png")    



class ThingList(LoginRequiredMixin, ListView):
    model = Thing
