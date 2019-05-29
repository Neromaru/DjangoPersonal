from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

# Create your views here.


class HelloWorldTemplateView(TemplateView):
    template_name = 'helloworld/helloworld_template.html'



def home_page_hello(request):
    return HttpResponse("hello World!")

