# Generated by Django 2.1.2 on 2019-08-22 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotations', '0002_auto_20190730_1620'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='annotation',
            options={'ordering': ['order']},
        ),
    ]