# Generated by Django 4.2.7 on 2023-11-13 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_auction_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='contact',
            field=models.TextField(default=7889307466),
        ),
        migrations.AlterField(
            model_name='auction',
            name='image',
            field=models.ImageField(blank=True, upload_to='item_images/'),
        ),
    ]
