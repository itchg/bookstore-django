import os
from myapp.formMoment import MomentForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse('<h1>welcome to myapp</h1>')

def test(request):
    return HttpResponse('<h1>test</h1>')

def moments_imput(request):
    if request.method == 'POST':
        form = MomentForm(request.POST)
        if form.is_valid():
            moment = form.save()
            moment.save()
            return HttpResponseRedirect(reverse('myapp.views.index'))
    else:
        form = MomentForm()
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return render(request, os.path.join(PROJECT_ROOT, 'myapp/templates/myapp/moments_input.html'), {'form': form})