# Generated by Django 4.2.5 on 2023-10-12 17:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tradehook', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventlog',
            name='received_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]