# Generated by Django 3.1.5 on 2021-01-18 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20210118_0419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='date_closed',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
