from django.views.generic import View
from django.shortcuts import render
from datetime import datetime, timedelta

from django.db.models import Max, Min, Avg, Q, FloatField
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
                      {'form': form})

    def post(self, request, *args, **kwargs):
        form = SearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            text = data['text_field']
            query_response, aggregation_results = self.query_string(text)
            avg, max_, min_, diff_ = aggregation_results.values()
            return self.check_query_status(request, query_response, form,
                                           avg, min_,
                                           max_, diff_)
        return render(request, 'django_personal/goods_list.html',
                      {'form': form})

    @staticmethod
    def calculate_percentage_diff(end_val, beg_value):
        return (end_val-beg_value)/beg_value*100

    def check_query_status(self, request, query_set, form, *args):
        query_results = query_set[:10]
        if query_results:
            return render(request, 'django_personal/goods_list.html',
                          {self.context_object_name: query_set,
                              'form': form,
                              'avg': args,
                              'min': args,
                              'max': args,
                              'diff': args,
                              'search': True})
        return render(request, 'django_personal/empty.html',
                      {'search': False,
                          'form': form})

    def query_string(self, text):
        django_format = "%Y-%m-%d"
        today = datetime.today()
        this_week = today - timedelta(days=today.weekday())
        last_week = today - timedelta(days=today.weekday(), weeks=1)
        aggregation_results = self.model.objects.filter(
            name__contains=text).aggregate(
            avg=Avg('price', output_field=FloatField(), filter=Q(
                published_date__gte=this_week
                )),
            max=Max('price', output_field=FloatField(), filter=Q(
                published_date__gte=this_week
                )),
            min=Min('price', output_field=FloatField(), filter=Q(
                published_date__gte=this_week
                )),
            diff=self.calculate_percentage_diff(Avg(
                'price', output_field=FloatField(), filter=Q(
                    published_date__gte=this_week
                    )
                ), Avg('price', output_field=FloatField(), filter=Q(
                    published_date__gte=last_week,
                    published_date__lt=this_week
                    )
                       )
                )
            )
        query_results = self.model.objects.filter(
            name__contains=text,
            published_date__gte=this_week
            )[:10]
        return query_results, aggregation_results
