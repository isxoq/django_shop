# Generated by Django 3.2.6 on 2021-09-03 06:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('translate', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='translate',
            old_name='translate',
            new_name='title',
        ),
    ]