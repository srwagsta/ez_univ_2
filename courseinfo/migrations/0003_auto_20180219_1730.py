# Generated by Django 2.0.2 on 2018-02-19 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseinfo', '0002_auto_20180219_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='nick_name',
            field=models.CharField(default='', max_length=45),
        ),
    ]
