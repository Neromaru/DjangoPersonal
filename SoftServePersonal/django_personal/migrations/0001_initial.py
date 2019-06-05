# Generated by Django 2.2.1 on 2019-06-05 11:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Good',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('product_url', models.TextField()),
                ('price', models.FloatField()),
                ('published_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Paltform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('base_url', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='GoodsToNotificateAbout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interested_max_price', models.FloatField()),
                ('interested_min_price', models.FloatField()),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_personal.Good')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='good',
            name='paltform',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_personal.Paltform'),
        ),
    ]
