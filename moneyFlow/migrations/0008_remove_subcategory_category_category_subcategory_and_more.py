# Generated by Django 5.1.6 on 2025-03-08 09:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moneyFlow', '0007_remove_category_subcategory_subcategory_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subcategory',
            name='category',
        ),
        migrations.AddField(
            model_name='category',
            name='subcategory',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='SubCategory', to='moneyFlow.subcategory', verbose_name='ПодКатегория'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Type', to='moneyFlow.type', verbose_name='Тип'),
        ),
    ]
