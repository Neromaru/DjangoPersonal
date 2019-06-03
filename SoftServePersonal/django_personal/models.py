from django.db import models as model

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
    user = model.ForeignKey(
        'users.CustomUser',
        on_delete=model.CASCADE
        )
    good = model.ForeignKey(
        'django_personal.Good',
        on_delete=model.CASCADE
        )

    def __str__(self):
        return f"{self.user.username}\t{self.good.name}\t" \
            f"{self.interested_max_price}\t{self.interested_min_price}"
