from django.forms import Form, CharField, FloatField


class SearchForm(Form):
    text_field = CharField(label='input search string')


class NotificationForm(Form):
    interested_max_price = FloatField(label='Upper price limit')
    interested_min_price = FloatField(label='Lower price limit')
    interested_good = CharField(label='Name of interested good')
