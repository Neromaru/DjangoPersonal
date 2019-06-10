from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DetailView, View, TemplateView
from django.urls import reverse_lazy
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import datetime


from .liqpay import LiqPay
from .forms import CustomUserCreationForm
from .models import CustomUser

# Create your views here.
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class ProfileView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    login_url = 'login'
    model = CustomUser
    template_name = 'profile/profile.html'

    def test_func(self):
        obj = self.get_object()
        return obj.id == self.request.user.id

class RrofileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    template_name = 'profile/edit.html'
    fields = ['username', 'first_name', 'last_name', 'email', 'image']
    login_url = 'login'

    def test_func(self):
        obj = self.get_object()
        return obj.id == self.request.user.id

    def get_success_url(self, **kwargs):
        return reverse_lazy('profile', kwargs={'pk': self.kwargs['pk']})


class SubscriptionPaymentView(TemplateView, LoginRequiredMixin,
                              UserPassesTestMixin,):
    template_name = 'profile/liqpay_button.html'

    def get(self, request, *args, **kwargs):
        back_url = 'https://terrible-pig-0.localtunnel.me'
        url = f'{back_url}/users/{request.user.pk}/subscription/confirmation/'
        liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY,
                        settings.LIQPAY_PRIVATE_KEY)
        params = {
            'action': 'pay',
            'amount': '5',
            'currency': 'USD',
            'description': f'{request.user.pk}',
            'version': '3',
            'sandbox': 1,
            'server_url': url
            }
        signature = liqpay.cnb_signature(params)
        data = liqpay.cnb_data(params)
        return render(request, self.template_name,
                      {'signature': signature, 'data': data})


@method_decorator(csrf_exempt, name='dispatch')
class PayCallbackView(View):
    model = CustomUser

    def post(self, request, *args, **kwargs):
        liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
        data = request.POST.get('data')
        signature = request.POST.get('signature')
        sign = liqpay.str_to_sign(settings.LIQPAY_PRIVATE_KEY + data + settings.LIQPAY_PRIVATE_KEY)
        if sign == signature:
            response = liqpay.decode_data_from_str(data)
            if response['status'] == 'success' or \
                response['status'] == 'sandbox':
                till = datetime.datetime.today() + datetime.timedelta(weeks=4)
                CustomUser.objects.filter(pk=kwargs['pk']).update(
                    subsctiption='p', subsctiption_due=till)
        return HttpResponse()




