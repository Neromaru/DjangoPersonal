# Generated by Django 2.2.1 on 2019-06-05 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20190605_1508'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='subsctiption',
            field=models.CharField(choices=[('c', 'Common'), ('p', 'Premium')], default='c', max_length=1),
        ),
        migrations.AddField(
            model_name='customuser',
            name='subsctiption_due',
            field=models.DateField(blank=True, null=True),
        ),
    ]
