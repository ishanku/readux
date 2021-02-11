# Generated by Django 2.2.10 on 2021-01-08 19:22

import uuid
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('manifests', '0014_auto_20210108_1619'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageServer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('server_base', models.CharField(default='https://loris.library.emory.edu', max_length=255)),
                ('storage_service', models.CharField(choices=[('sftp', 'SFTP'), ('s3', 'S3')], default='sftp', max_length=10)),
                ('storage_path', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='manifest',
            name='image_server',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='manifests.ImageServer'),
        ),
    ]