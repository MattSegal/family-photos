# Generated by Django 2.1.4 on 2018-12-15 05:18

import django.core.files.storage
from django.db import migrations, models
import photos.images


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0003_auto_20180225_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='optimized_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='local_file',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='/photos'), upload_to=photos.images.get_local_filename),
        ),
    ]
