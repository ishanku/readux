# Generated by Django 2.1.2 on 2019-12-17 19:52

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manifests', '0005_auto_20191115_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='manifest',
            name='search_vector',
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
        migrations.AddIndex(
            model_name='manifest',
            index=django.contrib.postgres.indexes.GinIndex(fields=['search_vector'], name='manifests_m_search__bd83b2_gin'),
        ),
    ]
