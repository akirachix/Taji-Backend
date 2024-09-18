# Generated by Django 5.1.1 on 2024-09-18 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PPBData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recall_date', models.DateField()),
                ('drug_name', models.CharField(max_length=255)),
                ('scientific_name', models.CharField(max_length=255)),
                ('batch_number', models.CharField(max_length=255)),
                ('manufacturer_name', models.CharField(max_length=255)),
                ('recall_reason', models.TextField()),
            ],
        ),
    ]
