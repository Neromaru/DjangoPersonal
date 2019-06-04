from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.views import View
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm, CutomUserChangeForm
from .models import CustomUser

# Create your views here.
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class ProfileView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, 'registration/profile.html')

class RrofileEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'registration/edit.html'
    fields = ['username', 'first_name', 'last_name', 'email', 'image']

    def get_success_url(self, **kwargs):
        return reverse_lazy('profile', kwargs={'pk': self.kwargs['pk']})


