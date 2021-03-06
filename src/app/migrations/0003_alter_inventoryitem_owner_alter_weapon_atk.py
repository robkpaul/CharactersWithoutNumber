# Generated by Django 4.0.3 on 2022-05-07 22:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_focus_options_remove_armor_equipped_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryitem',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to='app.character'),
        ),
        migrations.AlterField(
            model_name='weapon',
            name='atk',
            field=models.CharField(max_length=16),
        ),
    ]
