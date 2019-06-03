from django.forms import Form, CharField


class SearchForm(Form):
    text_field = CharField(label='input search string')
