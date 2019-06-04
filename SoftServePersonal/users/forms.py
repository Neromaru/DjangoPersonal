from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('username', 'email')


class CutomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'image')
