from django.contrib import admin

from .forms import CustomUserCreationForm, CutomUserChangeForm
from .models import CustomUser

from django.contrib.auth.admin import UserAdmin

class CutomAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CutomUserChangeForm
    list_display = ['email', 'username', 'image']

admin.site.register(CustomUser, CutomAdmin)

# Register your models here.
