from django.views.generic import TemplateView, ListView

from .models import Good
# Create your views here.


class IndexView(ListView):
    model = Good
    template_name = 'django_personal/goods_list.html'
    context_object_name = 'goods_list'

