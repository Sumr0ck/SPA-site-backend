# Generated by Django 4.2.1 on 2023-05-26 10:39

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(default=''),
        ),
        migrations.AddField(
            model_name='post',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(default=''),
        ),
    ]
