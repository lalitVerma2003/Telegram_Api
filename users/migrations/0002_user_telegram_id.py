# Generated by Django 5.1.6 on 2025-06-21 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='telegram_id',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]
