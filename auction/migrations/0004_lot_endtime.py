# Generated by Django 3.2 on 2023-05-30 16:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0003_alter_bid_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='lot',
            name='endtime',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
