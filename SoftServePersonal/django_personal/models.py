from django.db import models as model
from users.models import CustomUser

# Create your model here.


class Good(model.Model):
    name = model.TextField()
    paltform = model.ForeignKey(
        'django_personal.Paltform',
        on_delete=model.CASCADE
        )
    description = model.TextField()
    product_url = model.TextField()
    price = model.FloatField()
    published_date = model.DateField()

    def __str__(self):
        return self.name


class Paltform(model.Model):
    name = model.TextField()
    base_url = model.TextField()

    def __str__(self):
        return self.name


class GoodsToNotificateAbout(model.Model):
    interested_max_price = model.FloatField()
    interested_min_price = model.FloatField()
    interested_good = model.CharField(max_length=250, null=True, blank=True)
    user = model.OneToOneField(CustomUser, on_delete=model.CASCADE)

    def __str__(self):
        return f"{self.user.username}\t" \
            f"{self.interested_max_price}\t{self.interested_min_price}"
