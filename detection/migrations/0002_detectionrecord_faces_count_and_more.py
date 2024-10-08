# Generated by Django 5.1.1 on 2024-10-06 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detection', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='detectionrecord',
            name='faces_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='detectionrecord',
            name='processing_time',
            field=models.FloatField(default=0),
        ),
    ]
