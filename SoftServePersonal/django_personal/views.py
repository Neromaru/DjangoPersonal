from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
import datetime as dt

from .models import Good, GoodsToNotificateAbout
from .controllers import GoodsViewController, GoodsNotificationController
from .forms import SearchForm, NotificationForm
from users.models import CustomUser
# Create your views here.


class IndexView(View):
    model = Good
    form_class = SearchForm
    initial = {'key': 'value'}
    template_name = 'django_personal/goods_list.html'
    context_object_name = 'goods_list'
    controller = GoodsViewController()

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, 'django_personal/goods_list.html',
                      {"form": form})

    def post(self, request, *args, **kwargs):
        form = SearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            text = data['text_field']
            context = {'form': form, 'search': False}
            self.controller.text = text
            query_response = self.controller.query_interested_goods_for_users(
                limit=10)
            if query_response['success']:
                agregation_context = self.controller.query_goods_statistic()
                context.update(agregation_context)
                context['search'] = True
                context[self.context_object_name] = query_response
                return render(request, 'django_personal/goods_list.html',
                              context)
            return render(request, 'django_personal/empty.html',
                          context)
        return render(request, 'django_personal/goods_list.html',
                      {'form': form})


class NotificationView(AccessMixin, View):
    login_url = 'login'
    model = CustomUser
    form_class = NotificationForm
    template_name = 'django_personal/notification_page.html'
    initial = {'key': 'value'}
    controller = GoodsNotificationController()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not self.request.user.subsctiption == 'p' and not \
                self.request.user.subsctiption_due < dt.datetime.today():
            return HttpResponseRedirect(f'user/{request.user.pk}/subscription')

    def get(self, request, *args, **kwargs):
        form = self.form_class(self.initial)
        return render(request, self.template_name,
                      {'form': form})

    def post(self, request, *args, **kwargs):
        form = NotificationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            request.session['post_data'] = data
            data.update({'user': request.user})
            self.controller.add_notification(**data)
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/login')
