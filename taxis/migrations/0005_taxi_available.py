# Generated by Django 5.0.6 on 2024-06-24 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxis', '0004_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxi',
            name='available',
            field=models.BooleanField(default=True),
        ),
    ]
