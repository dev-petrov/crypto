# Generated by Django 3.1.1 on 2021-03-25 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0003_auto_20210301_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='algorythm',
            name='algo_num',
            field=models.IntegerField(default=0),
        ),
    ]
