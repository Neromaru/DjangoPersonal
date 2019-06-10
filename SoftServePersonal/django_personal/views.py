from django.views.generic import View, UpdateView, DeleteView
from django.shortcuts import render
from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.core.paginator import Paginator
import datetime as dt

from .models import Good, GoodsToNotificateAbout
from .controllers import GoodsViewController, GoodsNotificationController
from .forms import SearchForm, NotificationForm, GoodsToNotificateForm
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
                context[self.context_object_name] = query_response['results']
                return render(request, 'django_personal/goods_list.html',
                              context)
            return render(request, 'django_personal/empty.html',
                          context)
        return render(request, 'django_personal/goods_list.html',
                      {'form': form})


class AccessPremium(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.subsctiption_due:
            return HttpResponseRedirect(reverse_lazy(
                'subscription', kwargs={
                    'pk': request.user.pk
                    }
                )
                )
        if not request.user.subsctiption == 'p' and not \
                request.user.subsctiption_due < dt.datetime.today():
            return HttpResponseRedirect(reverse_lazy(
                'subscription', kwargs={
                    'pk': request.user.pk
                    }
                )
                )
        return super(AccessPremium, self).dispatch(
            request, *args, **kwargs)


class NotificationView(AccessPremium, View):
    login_url = 'login'
    model = CustomUser
    form_class = NotificationForm
    template_name = 'django_personal/notification_page.html'
    initial = {'key': 'value'}
    controller = GoodsNotificationController()

    def get(self, request, *args, **kwargs):
        form = self.form_class(self.initial)
        return render(request, self.template_name,
                      {'form': form})

    def post(self, request, *args, **kwargs):
        form = NotificationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data.update({'user': request.user})
            self.controller.add_notification(**data)
            return HttpResponseRedirect(reverse_lazy('notification_list',
                                                     kwargs={'pk':
                                                                 request.user.pk}))
        return HttpResponseRedirect('/login')


class NotifcationListView(AccessPremium, View):
    model = GoodsToNotificateAbout
    template_name = 'django_personal/notification_list.html'

    def get(self, request, *args, **kwargs):
        notifications = self.model.objects.filter(user=request.user)
        paginator = Paginator(notifications, 10)

        page = request.GET.get('page')
        notifications = paginator.get_page(page)
        return render(request, 'django_personal/notification_list.html',
                      {'notifications': notifications})


class EditNotificationView(AccessPremium, UpdateView):
    model = GoodsToNotificateAbout
    form_class = GoodsToNotificateForm
    template_name = 'django_personal/notification_page.html'


class DeleteNotificationView(AccessPremium, DeleteView):
    model = GoodsToNotificateAbout
    success_url = reverse_lazy('index')