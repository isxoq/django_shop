# Generated by Django 3.2.6 on 2021-08-28 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_order_orderproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='state',
            field=models.IntegerField(choices=[(1, 'Tolov kutilmoqda'), (2, 'Tolov bajarildi'), (3, 'Bekor qilindi'), (4, 'Tugatildi')]),
        ),
    ]
