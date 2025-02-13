# Generated by Django 4.2 on 2024-07-28 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_userqrcode_is_end'),
    ]

    operations = [
        migrations.AddField(
            model_name='userqrcode',
            name='cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='userqrcode',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userqrcode',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Book',
        ),
    ]
