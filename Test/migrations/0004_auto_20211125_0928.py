# Generated by Django 3.2.9 on 2021-11-25 03:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Test', '0003_alter_paper_test_start'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='question_attempt',
        ),
        migrations.RemoveField(
            model_name='result',
            name='question_left',
        ),
        migrations.RemoveField(
            model_name='result',
            name='question_wrong',
        ),
        migrations.AlterField(
            model_name='paper',
            name='test_start',
            field=models.DateField(default=datetime.datetime(2021, 11, 25, 9, 28, 46, 708105)),
        ),
    ]