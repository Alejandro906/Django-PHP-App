# Generated by Django 5.1.2 on 2024-10-16 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0006_alter_casa_options_casa_date_uploaded'),
    ]

    operations = [
        migrations.AddField(
            model_name='casa',
            name='recommended',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]