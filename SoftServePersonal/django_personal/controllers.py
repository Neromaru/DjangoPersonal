from datetime import datetime, timedelta
from django.db.models import Max, Min, Avg, Q, FloatField, Count
from .models import GoodsToNotificateAbout, Good
from plotly import graph_objs as go
from plotly import plotly as py
from plotly.offline import plot
from .tasks import email_notifications_for_users
from users.models import CustomUser


class GoodsViewController:
    goods_model = Good

    def __init__(self, text=None):
        self.text = text

    def query_interested_goods_for_users(self, offset=0, limit=10):
        today = datetime.today()
        this_week = today - timedelta(weeks=1)
        query_results = self.goods_model.objects.filter(
            name__contains=self.text,
            published_date__gte=this_week
            ).order_by('price')[offset:offset+limit]
        return {'success': True, 'results': query_results} if query_results \
            else {'success': False, 'results': []}

    def query_data_for_graph(self):
        two_weeks = datetime.today() - timedelta(weeks=2)
        graph_data = self.goods_model.objects.filter(
            published_date__gte=two_weeks).values('published_date',
                                                     'paltform')\
            .annotate(Avg('price')).order_by('published_date')
        return graph_data

    def create_graph(self, data):
        two_weeks = 15
        x_axis = [datetime.today().date() - timedelta(days=i) for i in range(
            two_weeks)][::-1]
        platforms = ['Olx', 'CraigsList', 'Ebay']
        graph_data = []
        for platform in platforms:
            platform_values = []
            for i in range(two_weeks):
                if data[i].get('published_date') == x_axis[i] and data[i].get(
                        'paltform') == platform:
                    platform_values.append(data.get('price__avg'))
            graph_data.append(platform_values)
        layout = go.Layout(barmode='group')
        fig = go.Figure(data=graph_data, layout=layout)
        return plot(fig, output_type='div')



    def query_goods_statistic(self):
        today = datetime.today()
        this_week = today - timedelta(weeks=1)
        last_week = today - timedelta(weeks=2)
        aggregation_results = self.goods_model.objects.filter(
            name__contains=self.text).aggregate(
            avg=Avg('price', output_field=FloatField(), filter=Q(
                published_date__gte=this_week
                )),
            max=Max('price', output_field=FloatField(), filter=Q(
                published_date__gte=this_week
                )),
            min=Min('price', output_field=FloatField(), filter=Q(
                published_date__gte=this_week
                )),
            diff=self._calculate_percentage_diff(Avg(
                'price', output_field=FloatField(), filter=Q(
                    published_date__gte=this_week
                    )
                ), Avg('price', output_field=FloatField(), filter=Q(
                    published_date__gte=last_week,
                    published_date__lt=this_week
                )
                       )
                ),
            total_results=Count('pk', filter=Q(name__contains=self.text))
            )
        return aggregation_results

    @staticmethod
    def _calculate_percentage_diff(end_val, beg_value):
        return (end_val - beg_value) / beg_value * 100


class GoodsNotificationController:
    model = GoodsToNotificateAbout
    model_good = Good

    def add_notification(self, **kwargs):
        notification = self.model(**kwargs)
        notification.save()
        return notification.pk



