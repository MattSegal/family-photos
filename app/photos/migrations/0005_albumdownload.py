# Generated by Django 2.1.4 on 2018-12-16 10:22

from django.db import migrations, models
import django.db.models.deletion
import photos.models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0004_auto_20181215_0518'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlbumDownload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('uploaded_at', models.DateTimeField(blank=True, null=True)),
                ('count_downloads', models.IntegerField(default=0)),
                ('file', models.FileField(blank=True, null=True, upload_to=photos.models.get_download_filename)),
                ('album', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='photos.Album')),
            ],
        ),
    ]
