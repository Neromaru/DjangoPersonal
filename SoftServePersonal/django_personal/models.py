from django.db import models as model
from users.models import CustomUser

# Create your model here.


class Good(model.Model):
    name = model.TextField()
    paltform = model.TextField()
    description = model.TextField()
    product_url = model.URLField()
    price = model.FloatField()
    published_date = model.DateField()

    def __str__(self):
        return self.name


class GoodsToNotificateAbout(model.Model):
    interested_max_price = model.FloatField()
    interested_min_price = model.FloatField()
    interested_good = model.CharField(max_length=250, null=True, blank=True)
    user = model.ForeignKey(CustomUser, on_delete=model.CASCADE)

    def __str__(self):
        return f"{self.user.username}\t" \
            f"{self.interested_max_price}\t{self.interested_min_price}"
