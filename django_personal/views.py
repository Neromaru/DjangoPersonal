from django.views.generic import TemplateView, ListView, View
from django.shortcuts import render

from .models import Good
from .forms import SearchForm
# Create your views here.


class IndexView(View):
    model = Good
    form_class = SearchForm
    initial = {'key':'value'}
    template_name = 'django_personal/goods_list.html'
    context_object_name = 'goods_list'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, 'django_personal/goods_list.html',
                      {self.context_object_name: self.model.objects.all(),
                       'form': form})

    def post(self, request, *args, **kwargs):
        form = SearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            text = data['text_field']
            response = self.model.objects.filter(name__contains=text)
            return render(request, 'django_personal/goods_list.html',
                          {self.context_object_name: response,
                              'form': form})
        return render(request, 'django_personal/goods_list.html',
                      {self.context_object_name: self.model.objects.all(),
                       'form': form})

