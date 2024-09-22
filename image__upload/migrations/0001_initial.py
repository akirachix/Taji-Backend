# Generated by Django 5.1.1 on 2024-09-19 10:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImageUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_file', models.ImageField(upload_to='uploads/')),
            ],
        ),
        migrations.CreateModel(
            name='TextExtraction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extracted_text', models.TextField()),
                ('processed_at', models.DateTimeField(auto_now_add=True)),
                ('image', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='text_extraction', to='image__upload.imageupload')),
            ],
        ),
    ]