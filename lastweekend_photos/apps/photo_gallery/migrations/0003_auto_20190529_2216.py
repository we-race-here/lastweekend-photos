# Generated by Django 2.2.1 on 2019-05-29 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo_gallery', '0002_auto_20190527_1156'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='sponsor',
        ),
        migrations.AddField(
            model_name='event',
            name='sponsors',
            field=models.ManyToManyField(blank=True, to='photo_gallery.Sponsor'),
        ),
    ]