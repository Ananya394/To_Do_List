# Generated by Django 5.1.7 on 2025-06-03 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routine', '0015_alter_activity_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='activity',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
