# Generated by Django 4.2.5 on 2023-10-03 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpg', '0008_alter_equipment_amulet_alter_equipment_boots_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='npc',
            name='enemy',
            field=models.BooleanField(default=False),
        ),
    ]
