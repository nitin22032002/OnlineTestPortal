# Generated by Django 3.2.9 on 2021-11-19 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User_website',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=20)),
                ('emailid', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=24)),
            ],
        ),
    ]