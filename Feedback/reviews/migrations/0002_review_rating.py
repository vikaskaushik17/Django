# Generated by Django 4.0.5 on 2022-07-11 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='rating',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]