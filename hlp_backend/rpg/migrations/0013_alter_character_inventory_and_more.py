# Generated by Django 4.2.5 on 2023-10-05 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpg', '0012_item_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='inventory',
            field=models.CharField(null=True),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='consumables',
            field=models.CharField(null=True),
        ),
    ]
