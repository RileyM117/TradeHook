# Generated by Django 4.2.6 on 2023-10-13 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tradehook', '0002_alter_eventlog_received_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerbrokers',
            name='broker_name',
            field=models.CharField(choices=[('Alpaca', 'Alpaca'), ('Alpaca - Paper', 'Alpaca - Paper')], max_length=255),
        ),
    ]