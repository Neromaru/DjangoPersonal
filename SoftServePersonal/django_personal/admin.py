from django.contrib import admin

from .models import Good, GoodsToNotificateAbout, Paltform


# Register your models here.
admin.site.register([Good, GoodsToNotificateAbout, Paltform])
