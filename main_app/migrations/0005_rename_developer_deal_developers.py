# Generated by Django 5.1.6 on 2025-02-06 20:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_alter_deal_asset_class'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deal',
            old_name='developer',
            new_name='developers',
        ),
    ]
