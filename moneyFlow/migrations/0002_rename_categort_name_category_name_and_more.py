# Generated by Django 5.1.6 on 2025-03-06 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moneyFlow', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='categort_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='status',
            old_name='status_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='subcategory',
            old_name='subcategory_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='type',
            old_name='type_name',
            new_name='name',
        ),
    ]
