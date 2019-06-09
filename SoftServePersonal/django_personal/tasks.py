from celery import shared_task, current_app
from django.core.mail import send_mail
from django.conf import settings
from .models import GoodsToNotificateAbout, Good
from django_celery_beat.models import PeriodicTask, CrontabSchedule


@shared_task
def delay_send_email():
    model = GoodsToNotificateAbout
    model_good = Good
    limit = 10
    for notification in model.objects.all().values(
            'interested_good', 'interested_min_price',
            'interested_max_price', 'user__email'):
        list_of_goods = model_good.objects.filter(
            name__contains=notification.interested_good,
            price__range=(notification.interested_min_price,
                          notification.interested_max_price)
            ).order_by('-price')[:limit]
        data = dict(goods_list=list_of_goods, email=notification.get(
            'user__email'))
        return send_email_to_user.delay(data)


@shared_task
def email_notifications_for_users():
    delay_send_email.delay()


@shared_task
def send_email_to_user(data):
    send_mail(
        'List of goods you were interested in',
        f'{data.get("goods_list")}',
        settings.EMAIL_HOST_USER,
        data.get('email')
        )


@shared_task
def math_pow(n):
    return 2 ** n

try:
    schedule, _ = CrontabSchedule.objects.update_or_create(
        minute='1',
        hour='*',
        day_of_week='*',
        day_of_month='*',
        month_of_year='*',
        )

    PeriodicTask.objects.update_or_create(
        crontab=schedule,
        name='Send emails',
        task='django_personal.tasks.email_notifications_for_users',
        )
except:
    pass
