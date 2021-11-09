# Generated by Django 3.2.9 on 2021-11-08 00:14

from django.db import migrations, models
import django.utils.crypto


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_alter_user_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='identifier',
            field=models.CharField(default=django.utils.crypto.get_random_string, max_length=12),
        ),
    ]