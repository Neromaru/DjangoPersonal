from datetime import datetime, timedelta
from django.db.models import Max, Min, Avg, Q, FloatField, Count
from .models import GoodsToNotificateAbout, Good
from .tasks import email_notifications_for_users
from users.models import CustomUser


class GoodsViewController:
    goods_model = Good

    def __init__(self, text=None):
        self.text = text

    def query_interested_goods_for_users(self, offset=0, limit=10):
        today = datetime.today()
        this_week = today - timedelta(days=today.weekday())
        query_results = self.goods_model.objects.filter(
            name__contains=self.text,
            published_date__gte=this_week
            ).order_by('-price')[offset:offset+limit]
        return {'success': True, 'results': query_results} if query_results \
            else {'success': False, 'results': []}

    def query_data_for_graph(self):
        graph_data = self.goods_model.objects.values('published_date',
                                                     'paltform__name')\
            .annotate(Avg('price'))
        pass

    def query_goods_statistic(self):
        today = datetime.today()
        this_week = today - timedelta(days=today.weekday())
        last_week = today - timedelta(days=today.weekday(), weeks=1)
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



