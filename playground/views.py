from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# request handlers

def calculate():
    x = 1
    y = 2
    return x

def say_hello(request):
    # next: need to map this view to a url
    # return HttpResponse('Hello World')
    x = calculate()
    return render(request, 'hello.html', {'name': 'Brydon'}) # now returning html content