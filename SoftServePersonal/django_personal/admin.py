from django.contrib import admin

from .models import Good, GoodsToNotificateAbout


# Register your models here.
admin.site.register([Good, GoodsToNotificateAbout])
