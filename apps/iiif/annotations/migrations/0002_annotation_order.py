# Generated by Django 2.1.2 on 2019-02-11 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotation',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
