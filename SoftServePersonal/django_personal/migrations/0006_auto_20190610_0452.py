# Generated by Django 2.2.1 on 2019-06-10 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_personal', '0005_auto_20190610_0249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='good',
            name='paltform',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='good',
            name='product_url',
            field=models.URLField(),
        ),
    ]
