# Generated by Django 4.0.3 on 2022-05-14 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_vocation_base_atk_alter_campaign_players_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='spell',
            name='school',
            field=models.CharField(default='high', max_length=32),
            preserve_default=False,
        ),
    ]
