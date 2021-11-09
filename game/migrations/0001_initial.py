# Generated by Django 3.2.9 on 2021-11-09 05:11

from django.db import migrations, models
import django.db.models.deletion
import django.utils.crypto


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=30)),
                ('balance', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=40)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.team')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(default=django.utils.crypto.get_random_string, max_length=12)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=30)),
                ('age', models.IntegerField()),
                ('market_value', models.IntegerField()),
                ('role', models.CharField(choices=[('gk', 'Goal Keeper'), ('de', 'Defender'), ('mf', 'Mid Fielder'), ('at', 'Attacker')], max_length=2)),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='game.team')),
            ],
        ),
    ]
