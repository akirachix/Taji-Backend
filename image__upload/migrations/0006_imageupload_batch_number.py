# Generated by Django 5.1.1 on 2024-09-20 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image__upload', '0005_imageupload_uploaded_at_delete_textextraction'),
    ]

    operations = [
        migrations.AddField(
            model_name='imageupload',
            name='batch_number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]