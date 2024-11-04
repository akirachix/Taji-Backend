# Generated by Django 5.0.7 on 2024-10-19 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacies', '0004_alter_pharmacy_reported'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pharmacy',
            old_name='address',
            new_name='pharmacyName',
        ),
        migrations.RemoveField(
            model_name='pharmacy',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='pharmacy',
            name='license_status',
        ),
        migrations.RemoveField(
            model_name='pharmacy',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='pharmacy',
            name='name',
        ),
        migrations.RemoveField(
            model_name='pharmacy',
            name='reported',
        ),
        migrations.AddField(
            model_name='pharmacy',
            name='county',
            field=models.CharField(default='Lifeblue', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pharmacy',
            name='town',
            field=models.CharField(default='Nairobi', max_length=100),
            preserve_default=False,
        ),
    ]