# Generated by Django 3.2.9 on 2021-11-19 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_website',
            name='emailid',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
