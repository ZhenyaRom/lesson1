# Generated by Django 5.1.4 on 2024-12-13 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seeds', '0004_alter_order_text_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='text_order',
            field=models.TextField(default='', verbose_name='Примечание'),
        ),
    ]
